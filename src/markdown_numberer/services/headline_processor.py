"""Headline processing and numbering integration."""

import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from ..core.models import ProcessingConfig, FileNumbering
from ..core.numbering import DefaultNumberingService
from ..core.exceptions import (
    MarkdownProcessingError,
    InvalidHeadlineError,
    ValidationError,
    create_exception_with_context
)
from ..core.logging import get_logger, log_function_call, log_function_result, log_exception
from .parser import MarkdownParser, MarkdownElement, ParsedMarkdown


@dataclass
class HeadlineProcessingResult:
    """Result of headline processing operation."""
    original_content: str
    processed_content: str
    headline_count: int
    headlines_processed: List[Dict[str, str]]
    stats: Dict[str, Any]


class HeadlineProcessor:
    """Process markdown headlines with numbering and validation."""
    
    def __init__(self, config: ProcessingConfig):
        """Initialize the headline processor.
        
        Args:
            config: Processing configuration
        """
        self.config = config
        self.numbering_service = DefaultNumberingService(config)
        self.parser = MarkdownParser(config)
        self.logger = get_logger(__name__)
    
    def process_headlines(self, content: str, file_numbering: FileNumbering) -> HeadlineProcessingResult:
        """Process headlines in markdown content.
        
        Args:
            content: Markdown content to process
            file_numbering: File numbering information
            
        Returns:
            HeadlineProcessingResult with processing results
            
        Raises:
            MarkdownProcessingError: If processing fails
        """
        log_function_call("process_headlines", content_length=len(content), file_number=file_numbering.file_number)
        
        try:
            # Parse the content
            parsed = self.parser.parse_content(content)
            
            # Process headlines
            processed_elements = []
            headlines_processed = []
            headline_count = 0
            
            for element in parsed.elements:
                if element.element_type == "headline":
                    # Check if headline level is within our range
                    if element.level >= self.config.start_level and element.level <= self.config.max_depth:
                        processed_element = self._process_headline_element(
                            element, file_numbering, headline_count
                        )
                        processed_elements.append(processed_element)
                        headlines_processed.append({
                            "level": str(element.level),
                            "original": element.content,
                            "numbered": processed_element.content
                        })
                        headline_count += 1
                    else:
                        # Keep original headline if not in range
                        processed_elements.append(element)
                else:
                    # Keep non-headline elements as-is
                    processed_elements.append(element)
            
            # Reconstruct content
            processed_content = self._reconstruct_content(processed_elements)
            
            # Calculate statistics
            stats = {
                "total_headlines_found": parsed.headline_count,
                "headlines_processed": headline_count,
                "headlines_skipped": parsed.headline_count - headline_count,
                "start_level": self.config.start_level,
                "max_depth": self.config.max_depth,
            }
            
            result = HeadlineProcessingResult(
                original_content=content,
                processed_content=processed_content,
                headline_count=headline_count,
                headlines_processed=headlines_processed,
                stats=stats
            )
            
            log_function_result("process_headlines", result, 0.0)  # Duration not tracked here
            return result
            
        except Exception as e:
            log_exception(
                self.logger,
                e,
                context={
                    "content_length": len(content),
                    "file_number": file_numbering.file_number,
                    "start_level": self.config.start_level,
                    "max_depth": self.config.max_depth
                }
            )
            raise create_exception_with_context(
                MarkdownProcessingError,
                "Failed to process headlines",
                context={
                    "content_length": len(content),
                    "file_number": file_numbering.file_number
                },
                cause=e
            )
    
    def _process_headline_element(
        self, 
        element: MarkdownElement, 
        file_numbering: FileNumbering,
        headline_index: int
    ) -> MarkdownElement:
        """Process a single headline element.
        
        Args:
            element: Headline element to process
            file_numbering: File numbering information
            headline_index: Index of this headline in the document
            
        Returns:
            Processed headline element
            
        Raises:
            InvalidHeadlineError: If headline processing fails
        """
        try:
            # Generate headline number
            headline_number = self._generate_headline_number(
                file_numbering, element.level, headline_index
            )
            
            # Create numbered headline content
            numbered_content = self._create_numbered_headline(
                element.content, headline_number, element.level
            )
            
            # Create new element with numbered content
            return MarkdownElement(
                element_type="headline",
                content=numbered_content,
                level=element.level,
                line_number=element.line_number
            )
        except Exception as e:
            log_exception(
                self.logger,
                e,
                context={
                    "headline_content": element.content,
                    "headline_level": element.level,
                    "line_number": element.line_number,
                    "headline_index": headline_index
                }
            )
            raise create_exception_with_context(
                InvalidHeadlineError,
                f"Failed to process headline at line {element.line_number}",
                context={
                    "headline_content": element.content,
                    "headline_level": element.level,
                    "line_number": element.line_number
                },
                cause=e
            )
    
    def _generate_headline_number(
        self, 
        file_numbering: FileNumbering, 
        level: int, 
        headline_index: int
    ) -> str:
        """Generate headline number based on file numbering and level.
        
        Args:
            file_numbering: File numbering information
            level: Headline level (1-6)
            headline_index: Index of headline in document
            
        Returns:
            Generated headline number
        """
        try:
            # Extract file number from the file numbering
            file_number = file_numbering.file_number
            
            # For now, use simple sequential numbering
            # In the future, this could be enhanced with hierarchical numbering
            headline_number = f"{file_number}.{headline_index + 1}"
            
            self.logger.debug(f"Generated headline number: {headline_number} for level {level}")
            
            return headline_number
        except Exception as e:
            log_exception(
                self.logger,
                e,
                context={
                    "file_number": file_numbering.file_number,
                    "level": level,
                    "headline_index": headline_index
                }
            )
            raise create_exception_with_context(
                InvalidHeadlineError,
                "Failed to generate headline number",
                context={
                    "file_number": file_numbering.file_number,
                    "level": level,
                    "headline_index": headline_index
                },
                cause=e
            )
    
    def _create_numbered_headline(
        self, 
        original_content: str, 
        headline_number: str, 
        level: int
    ) -> str:
        """Create numbered headline content.
        
        Args:
            original_content: Original headline text
            headline_number: Generated headline number
            level: Headline level
            
        Returns:
            Numbered headline content
        """
        try:
            # Clean the original content (remove leading/trailing whitespace)
            clean_content = original_content.strip()
            
            # Create the numbered headline
            numbered_headline = f"{headline_number} {clean_content}"
            
            self.logger.debug(f"Created numbered headline: {numbered_headline}")
            
            return numbered_headline
        except Exception as e:
            log_exception(
                self.logger,
                e,
                context={
                    "original_content": original_content,
                    "headline_number": headline_number,
                    "level": level
                }
            )
            raise create_exception_with_context(
                InvalidHeadlineError,
                "Failed to create numbered headline",
                context={
                    "original_content": original_content,
                    "headline_number": headline_number,
                    "level": level
                },
                cause=e
            )
    
    def _reconstruct_content(self, elements: List[MarkdownElement]) -> str:
        """Reconstruct markdown content from processed elements.
        
        Args:
            elements: List of processed markdown elements
            
        Returns:
            Reconstructed markdown content
        """
        try:
            lines = []
            
            for element in elements:
                if element.element_type == "headline":
                    # Add headline with appropriate number of # symbols
                    headline_marker = "#" * element.level
                    lines.append(f"{headline_marker} {element.content}")
                elif element.element_type == "paragraph":
                    lines.append(element.content)
                elif element.element_type == "list_item":
                    # Preserve list item formatting
                    if element.metadata and "marker" in element.metadata:
                        indent = " " * element.metadata.get("indent", 0)
                        marker = element.metadata["marker"]
                        lines.append(f"{indent}{marker} {element.content}")
                    else:
                        lines.append(f"- {element.content}")
                elif element.element_type == "code_block_start":
                    lines.append(element.content)
                elif element.element_type == "code_block_content":
                    lines.append(element.content)
                elif element.element_type == "code_block_end":
                    lines.append(element.content)
                elif element.element_type == "table_row":
                    lines.append(element.content)
                elif element.element_type == "horizontal_rule":
                    lines.append(element.content)
                elif element.element_type == "empty":
                    lines.append("")
            
            return "\n".join(lines)
        except Exception as e:
            log_exception(
                self.logger,
                e,
                context={"element_count": len(elements)}
            )
            raise create_exception_with_context(
                MarkdownProcessingError,
                "Failed to reconstruct content",
                context={"element_count": len(elements)},
                cause=e
            )
    
    def validate_headlines(self, content: str) -> List[str]:
        """Validate headlines in markdown content.
        
        Args:
            content: Markdown content to validate
            
        Returns:
            List of validation error messages
        """
        log_function_call("validate_headlines", content_length=len(content))
        
        try:
            errors = []
            parsed = self.parser.parse_content(content)
            
            for element in parsed.elements:
                if element.element_type == "headline":
                    # Check for empty headlines
                    if not element.content.strip():
                        errors.append(f"Empty headline at line {element.line_number}")
                    
                    # Check headline level range
                    if element.level < 1 or element.level > 6:
                        errors.append(f"Invalid headline level {element.level} at line {element.line_number}")
            
            log_function_result("validate_headlines", {"error_count": len(errors)}, 0.0)
            return errors
        except Exception as e:
            log_exception(
                self.logger,
                e,
                context={"content_length": len(content)}
            )
            raise create_exception_with_context(
                ValidationError,
                "Failed to validate headlines",
                context={"content_length": len(content)},
                cause=e
            )
    
    def get_headline_statistics(self, content: str) -> Dict[str, int]:
        """Get statistics about headlines in markdown content.
        
        Args:
            content: Markdown content to analyze
            
        Returns:
            Dictionary with headline statistics
        """
        log_function_call("get_headline_statistics", content_length=len(content))
        
        try:
            parsed = self.parser.parse_content(content)
            
            stats = {
                "total_headlines": 0,
                "headlines_by_level": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
                "empty_headlines": 0,
                "headlines_in_range": 0
            }
            
            for element in parsed.elements:
                if element.element_type == "headline":
                    stats["total_headlines"] += 1
                    stats["headlines_by_level"][element.level] += 1
                    
                    if not element.content.strip():
                        stats["empty_headlines"] += 1
                    
                    if element.level >= self.config.start_level and element.level <= self.config.max_depth:
                        stats["headlines_in_range"] += 1
            
            log_function_result("get_headline_statistics", stats, 0.0)
            return stats
        except Exception as e:
            log_exception(
                self.logger,
                e,
                context={"content_length": len(content)}
            )
            raise create_exception_with_context(
                MarkdownProcessingError,
                "Failed to get headline statistics",
                context={"content_length": len(content)},
                cause=e
            ) 