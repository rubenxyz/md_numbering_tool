"""Markdown parsing and content processing functionality."""

import re
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass

from ..core.models import ProcessingConfig, FileNumbering
from ..core.numbering import DefaultNumberingService
from ..core.exceptions import (
    FileNotFoundError,
    FileReadError,
    MarkdownParseError,
    MarkdownValidationError,
    InvalidHeadlineError,
    create_exception_with_context
)
from ..core.logging import get_logger, log_function_call, log_function_result, log_exception


@dataclass
class MarkdownElement:
    """Represents a markdown element with its type and content."""
    element_type: str  # 'headline', 'paragraph', 'code_block', 'list', etc.
    level: Optional[int] = None  # For headlines: 1-6, for lists: nesting level
    content: str = ""
    line_number: int = 0
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ParsedMarkdown:
    """Represents parsed markdown content with elements and metadata."""
    elements: List[MarkdownElement]
    total_lines: int
    headline_count: int
    content_length: int
    metadata: Dict[str, Any]


class MarkdownParser:
    """Markdown parser for identifying headlines and preserving content structure."""
    
    def __init__(self, config: ProcessingConfig):
        """Initialize the markdown parser with configuration."""
        self.config = config
        self.numbering_service = DefaultNumberingService(config)
        self.logger = get_logger(__name__)
        
        # Regex patterns for different markdown elements
        self.headline_pattern = re.compile(r'^(#{1,6})\s*(.*)$')
        self.code_block_pattern = re.compile(r'^```[\w]*$')
        self.list_pattern = re.compile(r'^(\s*)([-*+]|\d+\.)\s+(.+)$')
        self.table_pattern = re.compile(r'^\|(.+)\|$')
        self.horizontal_rule_pattern = re.compile(r'^[-*_]{3,}$')
        self.link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        self.image_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
        self.bold_pattern = re.compile(r'\*\*([^*]+)\*\*')
        self.italic_pattern = re.compile(r'\*([^*]+)\*')
        self.code_inline_pattern = re.compile(r'`([^`]+)`')
    
    def parse_file(self, file_path: Path) -> ParsedMarkdown:
        """Parse a markdown file and return structured content.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            ParsedMarkdown object with elements and metadata
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            FileReadError: If the file can't be read
            MarkdownParseError: If parsing fails
        """
        log_function_call("parse_file", file_path=str(file_path))
        
        try:
            # Validate file exists
            if not file_path.exists():
                raise create_exception_with_context(
                    FileNotFoundError,
                    f"File not found: {file_path}",
                    context={"file_path": str(file_path)}
                )
            
            if not file_path.is_file():
                raise create_exception_with_context(
                    FileReadError,
                    f"Path is not a file: {file_path}",
                    context={"file_path": str(file_path)}
                )
            
            # Read file content with proper error handling
            content = self._read_file_content(file_path)
            
            # Parse the content
            result = self.parse_content(content, file_path)
            
            log_function_result("parse_file", result, 0.0)  # Duration not tracked here
            return result
            
        except (FileNotFoundError, FileReadError):
            # Re-raise these specific exceptions as-is
            raise
        except Exception as e:
            # Wrap other exceptions in MarkdownParseError
            raise create_exception_with_context(
                MarkdownParseError,
                f"Failed to parse file: {file_path}",
                context={"file_path": str(file_path)},
                cause=e
            )
    
    def _read_file_content(self, file_path: Path) -> str:
        """Read file content with proper encoding handling.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            File content as string
            
        Raises:
            FileReadError: If the file can't be read or decoded
        """
        encodings = ['utf-8', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                return file_path.read_text(encoding=encoding)
            except UnicodeDecodeError as e:
                self.logger.debug(f"Failed to decode {file_path} with {encoding}: {e}")
                continue
            except Exception as e:
                raise create_exception_with_context(
                    FileReadError,
                    f"Failed to read file: {file_path}",
                    context={"file_path": str(file_path), "encoding": encoding},
                    cause=e
                )
        
        # If we get here, all encodings failed
        raise create_exception_with_context(
            FileReadError,
            f"Unable to decode file with any encoding: {file_path}",
            context={"file_path": str(file_path), "tried_encodings": encodings}
        )
    
    def parse_content(self, content: str, file_path: Optional[Path] = None) -> ParsedMarkdown:
        """Parse markdown content and return structured elements.
        
        Args:
            content: Markdown content as string
            file_path: Optional file path for context
            
        Returns:
            ParsedMarkdown object with elements and metadata
            
        Raises:
            MarkdownParseError: If parsing fails
        """
        log_function_call("parse_content", content_length=len(content), file_path=str(file_path) if file_path else None)
        
        try:
            lines = content.split('\n')
            elements = []
            headline_count = 0
            in_code_block = False
            code_block_language = ""
            
            for line_number, line in enumerate(lines, 1):
                try:
                    element = self._parse_line(line, line_number, in_code_block)
                    
                    if element.element_type == 'code_block_start':
                        in_code_block = True
                        code_block_language = element.metadata.get('language', '')
                        elements.append(element)  # Include the start marker
                        continue
                    elif element.element_type == 'code_block_end':
                        in_code_block = False
                        elements.append(element)  # Include the end marker
                        continue
                    elif in_code_block:
                        element.element_type = 'code_block_content'
                        element.metadata = {'language': code_block_language}
                    
                    if element.element_type == 'headline':
                        headline_count += 1
                    
                    elements.append(element)
                    
                except Exception as e:
                    # Log the error but continue parsing
                    log_exception(
                        self.logger,
                        e,
                        context={
                            "line_number": line_number,
                            "line_content": line[:100],  # Truncate long lines
                            "file_path": str(file_path) if file_path else None
                        },
                        level="WARNING"
                    )
                    # Add a placeholder element to maintain line count
                    elements.append(MarkdownElement(
                        element_type='error',
                        content=f"Error parsing line {line_number}",
                        line_number=line_number,
                        metadata={'error': str(e)}
                    ))
            
            # Calculate metadata
            metadata = {
                'file_path': str(file_path) if file_path else None,
                'encoding': 'utf-8',
                'line_count': len(lines),
                'headline_count': headline_count,
                'content_length': len(content),
            }
            
            result = ParsedMarkdown(
                elements=elements,
                total_lines=len(lines),
                headline_count=headline_count,
                content_length=len(content),
                metadata=metadata
            )
            
            log_function_result("parse_content", result, 0.0)  # Duration not tracked here
            return result
            
        except Exception as e:
            raise create_exception_with_context(
                MarkdownParseError,
                f"Failed to parse markdown content",
                context={"file_path": str(file_path) if file_path else None},
                cause=e
            )
    
    def _parse_line(self, line: str, line_number: int, in_code_block: bool) -> MarkdownElement:
        """Parse a single line and determine its markdown element type.
        
        Args:
            line: The line to parse
            line_number: Line number for context
            in_code_block: Whether we're currently in a code block
            
        Returns:
            MarkdownElement representing the parsed line
        """
        # Handle code block boundaries
        if self.code_block_pattern.match(line):
            if in_code_block:
                return MarkdownElement(
                    element_type='code_block_end',
                    content=line,
                    line_number=line_number
                )
            else:
                language = line[3:].strip() if len(line) > 3 else ""
                return MarkdownElement(
                    element_type='code_block_start',
                    content=line,
                    line_number=line_number,
                    metadata={'language': language}
                )
        
        # Handle headlines
        headline_match = self.headline_pattern.match(line)
        if headline_match:
            level = len(headline_match.group(1))
            content = headline_match.group(2).strip()  # Strip whitespace
            return MarkdownElement(
                element_type='headline',
                level=level,
                content=content,
                line_number=line_number
            )
        
        # Handle horizontal rules
        if self.horizontal_rule_pattern.match(line):
            return MarkdownElement(
                element_type='horizontal_rule',
                content=line,
                line_number=line_number
            )
        
        # Handle lists
        list_match = self.list_pattern.match(line)
        if list_match:
            indent = len(list_match.group(1))
            marker = list_match.group(2)
            content = list_match.group(3)
            level = indent // 2 + 1  # Estimate nesting level
            
            return MarkdownElement(
                element_type='list_item',
                level=level,
                content=content,
                line_number=line_number,
                metadata={'marker': marker, 'indent': indent}
            )
        
        # Handle tables
        if self.table_pattern.match(line):
            return MarkdownElement(
                element_type='table_row',
                content=line,
                line_number=line_number
            )
        
        # Handle empty lines
        if not line.strip():
            return MarkdownElement(
                element_type='empty',
                content=line,
                line_number=line_number
            )
        
        # Default to paragraph
        return MarkdownElement(
            element_type='paragraph',
            content=line,
            line_number=line_number
        )
    
    def process_file_with_numbering(self, file_path: Path, output_dir: Path) -> Tuple[str, int]:
        """Process a markdown file with headline numbering.
        
        Args:
            file_path: Path to the input markdown file
            output_dir: Output directory for processed files
            
        Returns:
            Tuple of (processed_content, headline_count)
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            FileReadError: If the file can't be read
            MarkdownParseError: If parsing fails
        """
        log_function_call("process_file_with_numbering", file_path=str(file_path), output_dir=str(output_dir))
        
        try:
            # Create file numbering
            file_numbering = self.numbering_service.create_file_numbering(file_path, output_dir)
            
            # Read and parse the file
            parsed = self.parse_file(file_path)
            
            # Apply headline numbering
            processed_content, headline_count = self.numbering_service.number_headlines(
                file_path.read_text(encoding='utf-8'),
                file_numbering.file_number
            )
            
            log_function_result("process_file_with_numbering", {"headline_count": headline_count}, 0.0)
            return processed_content, headline_count
            
        except (FileNotFoundError, FileReadError, MarkdownParseError):
            # Re-raise these specific exceptions as-is
            raise
        except Exception as e:
            raise create_exception_with_context(
                MarkdownParseError,
                f"Failed to process file with numbering: {file_path}",
                context={"file_path": str(file_path), "output_dir": str(output_dir)},
                cause=e
            )
    
    def validate_markdown_structure(self, parsed: ParsedMarkdown) -> List[str]:
        """Validate markdown structure for common issues.
        
        Args:
            parsed: ParsedMarkdown object to validate
            
        Returns:
            List of validation error messages
        """
        log_function_call("validate_markdown_structure", element_count=len(parsed.elements))
        
        try:
            errors = []
            
            # Check for proper headline hierarchy
            headline_levels = [elem.level for elem in parsed.elements if elem.element_type == 'headline']
            
            for i, level in enumerate(headline_levels):
                if i > 0 and level > headline_levels[i-1] + 1:
                    errors.append(f"Invalid headline hierarchy at line {parsed.elements[i].line_number}: "
                                f"Jumped from level {headline_levels[i-1]} to {level}")
            
            # Check for empty headlines
            for elem in parsed.elements:
                if elem.element_type == 'headline' and not elem.content:
                    errors.append(f"Empty headline at line {elem.line_number}")
            
            # Check for very long lines (potential formatting issues)
            for elem in parsed.elements:
                if len(elem.content) > 1000:  # Arbitrary limit
                    errors.append(f"Very long line at line {elem.line_number}: {len(elem.content)} characters")
            
            log_function_result("validate_markdown_structure", {"error_count": len(errors)}, 0.0)
            return errors
            
        except Exception as e:
            log_exception(self.logger, e, context={"parsed_elements": len(parsed.elements)})
            raise create_exception_with_context(
                MarkdownValidationError,
                "Failed to validate markdown structure",
                context={"element_count": len(parsed.elements)},
                cause=e
            )
    
    def extract_headlines(self, parsed: ParsedMarkdown) -> List[MarkdownElement]:
        """Extract all headlines from parsed markdown.
        
        Args:
            parsed: ParsedMarkdown object
            
        Returns:
            List of headline elements
        """
        try:
            headlines = [elem for elem in parsed.elements if elem.element_type == 'headline']
            self.logger.debug(f"Extracted {len(headlines)} headlines from {len(parsed.elements)} elements")
            return headlines
        except Exception as e:
            log_exception(self.logger, e, context={"parsed_elements": len(parsed.elements)})
            raise create_exception_with_context(
                MarkdownParseError,
                "Failed to extract headlines",
                context={"element_count": len(parsed.elements)},
                cause=e
            )
    
    def get_headline_hierarchy(self, parsed: ParsedMarkdown) -> List[Dict[str, Any]]:
        """Get the headline hierarchy with levels and content.
        
        Args:
            parsed: ParsedMarkdown object
            
        Returns:
            List of headline dictionaries with level, content, and line number
        """
        try:
            headlines = self.extract_headlines(parsed)
            hierarchy = [
                {
                    'level': elem.level,
                    'content': elem.content,
                    'line_number': elem.line_number,
                    'line': f"{'#' * elem.level} {elem.content}"
                }
                for elem in headlines
            ]
            self.logger.debug(f"Generated headline hierarchy with {len(hierarchy)} levels")
            return hierarchy
        except Exception as e:
            log_exception(self.logger, e, context={"parsed_elements": len(parsed.elements)})
            raise create_exception_with_context(
                MarkdownParseError,
                "Failed to get headline hierarchy",
                context={"element_count": len(parsed.elements)},
                cause=e
            )
    
    def count_elements_by_type(self, parsed: ParsedMarkdown) -> Dict[str, int]:
        """Count elements by their type.
        
        Args:
            parsed: ParsedMarkdown object
            
        Returns:
            Dictionary mapping element types to counts
        """
        try:
            counts = {}
            for elem in parsed.elements:
                elem_type = elem.element_type
                counts[elem_type] = counts.get(elem_type, 0) + 1
            
            self.logger.debug(f"Element counts: {counts}")
            return counts
        except Exception as e:
            log_exception(self.logger, e, context={"parsed_elements": len(parsed.elements)})
            raise create_exception_with_context(
                MarkdownParseError,
                "Failed to count elements by type",
                context={"element_count": len(parsed.elements)},
                cause=e
            )
    
    def preserve_formatting(self, content: str) -> str:
        """Preserve original formatting while processing.
        
        Args:
            content: Original markdown content
            
        Returns:
            Content with preserved formatting
        """
        try:
            # This is a placeholder for formatting preservation logic
            # In a real implementation, this would handle various formatting edge cases
            return content
        except Exception as e:
            log_exception(self.logger, e, context={"content_length": len(content)})
            raise create_exception_with_context(
                MarkdownParseError,
                "Failed to preserve formatting",
                context={"content_length": len(content)},
                cause=e
            )
    
    def detect_markdown_features(self, parsed: ParsedMarkdown) -> Dict[str, Any]:
        """Detect markdown features and return metadata.
        
        Args:
            parsed: ParsedMarkdown object
            
        Returns:
            Dictionary of detected features
        """
        try:
            features = {
                'has_headlines': any(elem.element_type == 'headline' for elem in parsed.elements),
                'has_code_blocks': any(elem.element_type in ['code_block_start', 'code_block_content'] for elem in parsed.elements),
                'has_lists': any(elem.element_type == 'list_item' for elem in parsed.elements),
                'has_tables': any(elem.element_type == 'table_row' for elem in parsed.elements),
                'has_links': any(self.link_pattern.search(elem.content) for elem in parsed.elements if elem.content),
                'has_images': any(self.image_pattern.search(elem.content) for elem in parsed.elements if elem.content),
                'max_headline_level': max([elem.level for elem in parsed.elements if elem.element_type == 'headline'] or [0]),
                'total_elements': len(parsed.elements),
            }
            
            self.logger.debug(f"Detected features: {features}")
            return features
        except Exception as e:
            log_exception(self.logger, e, context={"parsed_elements": len(parsed.elements)})
            raise create_exception_with_context(
                MarkdownParseError,
                "Failed to detect markdown features",
                context={"element_count": len(parsed.elements)},
                cause=e
            ) 