"""Core numbering logic for markdown files and headlines."""

import re
from pathlib import Path
from typing import List, Optional, Tuple

from .models import FileNumbering, ProcessingConfig, SortingMethod


class DefaultNumberingService:
    """Default implementation of numbering logic for markdown files and headlines."""
    
    def __init__(self, config: ProcessingConfig):
        """Initialize the numbering service with configuration."""
        self.config = config
        self._folder_number_cache: dict[Path, str] = {}
        self._file_counter_cache: dict[str, int] = {}
    
    def extract_folder_number(self, folder_path: Path) -> str:
        """Extract the hierarchical number from a folder name.
        
        Args:
            folder_path: Path to the folder
            
        Returns:
            The folder number (e.g., "00.1", "01.2.3") or empty string if no number found
        """
        if folder_path in self._folder_number_cache:
            return self._folder_number_cache[folder_path]
        
        folder_name = folder_path.name
        
        # Pattern to match numbers at the start of folder names
        # Supports formats like: "00.1", "01.2.3", "1.2", "01", etc.
        pattern = r'^(\d+(?:\.\d+)*)'
        match = re.match(pattern, folder_name)
        
        if match:
            folder_number = match.group(1)
            self._folder_number_cache[folder_path] = folder_number
            return folder_number
        
        # If no number found, return empty string
        self._folder_number_cache[folder_path] = ""
        return ""
    
    def generate_file_number(self, file_path: Path, folder_number: str) -> str:
        """Generate a file number based on the folder number and file position.
        
        Args:
            file_path: Path to the file
            folder_number: The folder's hierarchical number
            
        Returns:
            The file number (e.g., "00.1.1", "01.2.3.1")
        """
        # Get the parent folder path for cache key
        parent_folder = file_path.parent
        
        # Create cache key for this folder
        cache_key = f"{parent_folder}_{folder_number}"
        
        # Increment file counter for this folder
        if cache_key in self._file_counter_cache:
            self._file_counter_cache[cache_key] += 1
        else:
            self._file_counter_cache[cache_key] = 1
        
        file_index = self._file_counter_cache[cache_key]
        
        # Generate file number
        if folder_number:
            file_number = f"{folder_number}.{file_index}"
        else:
            # If no folder number, use just the file index
            file_number = f"{file_index:02d}"
        
        return file_number
    
    def sort_files(self, files: List[Path]) -> List[Path]:
        """Sort files according to the configured sorting method.
        
        Args:
            files: List of file paths to sort
            
        Returns:
            Sorted list of file paths
        """
        if not files:
            return files
        
        if self.config.sorting_method == SortingMethod.ALPHABETICAL:
            return sorted(files, key=lambda f: f.name.lower())
        
        elif self.config.sorting_method == SortingMethod.CREATION_DATE:
            return sorted(files, key=lambda f: f.stat().st_ctime)
        
        elif self.config.sorting_method == SortingMethod.MODIFICATION_DATE:
            return sorted(files, key=lambda f: f.stat().st_mtime)
        
        elif self.config.sorting_method == SortingMethod.SIZE:
            return sorted(files, key=lambda f: f.stat().st_size)
        
        elif self.config.sorting_method == SortingMethod.CUSTOM:
            # For custom sorting, we'll use alphabetical as default
            # This can be extended with custom sorting logic
            return sorted(files, key=lambda f: f.name.lower())
        
        else:
            # Default to alphabetical
            return sorted(files, key=lambda f: f.name.lower())
    
    def create_file_numbering(self, file_path: Path, output_dir: Path) -> FileNumbering:
        """Create a FileNumbering instance for a given file.
        
        Args:
            file_path: Path to the input file
            output_dir: Output directory path
            
        Returns:
            FileNumbering instance with all numbering information
        """
        # Extract folder number from parent directory
        parent_folder = file_path.parent
        folder_number = self.extract_folder_number(parent_folder)
        
        # Generate file number
        file_number = self.generate_file_number(file_path, folder_number)
        
        # Extract file information
        original_name = file_path.stem
        extension = file_path.suffix
        
        # Create numbered filename
        if self.config.preserve_original_name:
            numbered_filename = f"{file_number}{self.config.filename_separator}{original_name}{extension}"
        else:
            numbered_filename = f"{file_number}{extension}"
        
        # Create output path
        numbered_path = output_dir / numbered_filename
        
        return FileNumbering(
            original_path=file_path,
            numbered_path=numbered_path,
            file_number=file_number,
            folder_number=folder_number,
            original_name=original_name,
            extension=extension
        )
    
    def number_headlines(self, content: str, file_number: str) -> Tuple[str, int]:
        """Number headlines in markdown content.
        
        Args:
            content: The markdown content to process
            file_number: The file's hierarchical number
            
        Returns:
            Tuple of (modified_content, headline_count)
        """
        if not content:
            return content, 0
        
        lines = content.split('\n')
        modified_lines = []
        headline_count = 0
        level_counters = {}
        
        for line in lines:
            # Check if line is a headline (starts with #)
            headline_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            
            if headline_match:
                level = len(headline_match.group(1))
                headline_text = headline_match.group(2)
                
                # Skip if level is outside our range
                if level < self.config.start_level or level > self.config.max_depth:
                    modified_lines.append(line)
                    continue
                
                # Check if we should preserve existing numbering
                if self.config.preserve_existing:
                    # Check if headline already has a number
                    existing_number_match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)$', headline_text)
                    if existing_number_match:
                        modified_lines.append(line)
                        continue
                
                # Generate headline number
                headline_number = self._generate_headline_number(
                    file_number, level, level_counters
                )
                
                # Create numbered headline
                numbered_headline = f"{headline_match.group(1)} {headline_number} {headline_text}"
                modified_lines.append(numbered_headline)
                headline_count += 1
                
            else:
                modified_lines.append(line)
        
        return '\n'.join(modified_lines), headline_count
    
    def _generate_headline_number(self, file_number: str, level: int, level_counters: dict) -> str:
        """Generate a headline number based on file number and level.
        
        Args:
            file_number: The file's hierarchical number
            level: The headline level (1-6)
            level_counters: Dictionary tracking counters for each level
            
        Returns:
            The headline number (e.g., "00.1.1.1", "00.1.1.2")
        """
        # Use a single counter for all headlines, regardless of level
        if 'total' not in level_counters:
            level_counters['total'] = 0
        
        # Increment total counter
        level_counters['total'] += 1
        
        # Build the headline number
        if file_number:
            headline_number = f"{file_number}.{level_counters['total']}"
        else:
            headline_number = f"{level_counters['total']:02d}"
        
        return headline_number
    
    def validate_numbering_consistency(self, file_numberings: List[FileNumbering]) -> List[str]:
        """Validate that numbering is consistent across all files.
        
        Args:
            file_numberings: List of FileNumbering instances
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        # Check for duplicate file numbers
        file_numbers = [fn.file_number for fn in file_numberings]
        duplicates = [num for num in set(file_numbers) if file_numbers.count(num) > 1]
        
        if duplicates:
            errors.append(f"Duplicate file numbers found: {duplicates}")
        
        # Check for duplicate output paths
        output_paths = [fn.numbered_path for fn in file_numberings]
        duplicate_paths = [path for path in set(output_paths) if output_paths.count(path) > 1]
        
        if duplicate_paths:
            errors.append(f"Duplicate output paths found: {duplicate_paths}")
        
        # Check for invalid file numbers (should be hierarchical)
        for fn in file_numberings:
            if not self._is_valid_hierarchical_number(fn.file_number):
                errors.append(f"Invalid file number format: {fn.file_number}")
        
        return errors
    
    def _is_valid_hierarchical_number(self, number: str) -> bool:
        """Check if a number follows valid hierarchical format.
        
        Args:
            number: The number to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Pattern for hierarchical numbers: digits separated by dots
        pattern = r'^\d+(?:\.\d+)*$'
        return bool(re.match(pattern, number))
    
    def reset_counters(self) -> None:
        """Reset all internal counters and caches."""
        self._folder_number_cache.clear()
        self._file_counter_cache.clear() 