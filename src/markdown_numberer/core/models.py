"""Core data models for markdown numbering system."""

from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator


class SortingMethod(str, Enum):
    """Enumeration of available file sorting methods."""
    
    ALPHABETICAL = "alphabetical"
    CREATION_DATE = "creation_date"
    MODIFICATION_DATE = "modification_date"
    SIZE = "size"
    CUSTOM = "custom"


class FileNumbering(BaseModel):
    """Model representing file numbering information."""
    
    original_path: Path = Field(..., description="Original file path")
    numbered_path: Path = Field(..., description="New numbered file path")
    file_number: str = Field(..., description="Assigned file number (e.g., '00.1.1')")
    folder_number: str = Field(..., description="Parent folder number (e.g., '00.1')")
    original_name: str = Field(..., description="Original filename without extension")
    extension: str = Field(..., description="File extension")
    
    @field_validator("original_path", "numbered_path", mode="before")
    @classmethod
    def validate_paths(cls, v: Any) -> Path:
        """Convert string paths to Path objects."""
        if isinstance(v, str):
            return Path(v)
        return v
    
    @property
    def full_number(self) -> str:
        """Get the full hierarchical number for this file."""
        return f"{self.file_number}"
    
    @property
    def numbered_filename(self) -> str:
        """Get the numbered filename with extension."""
        return f"{self.file_number}-{self.original_name}{self.extension}"


class ProcessingResult(BaseModel):
    """Model representing the result of processing a single file."""
    
    file_numbering: FileNumbering = Field(..., description="File numbering information")
    success: bool = Field(..., description="Whether processing was successful")
    error_message: Optional[str] = Field(None, description="Error message if processing failed")
    processing_time: float = Field(..., description="Processing time in seconds")
    file_size: int = Field(..., description="File size in bytes")
    headline_count: int = Field(0, description="Number of headlines processed")
    content_modified: bool = Field(False, description="Whether file content was modified")
    
    @field_validator("processing_time")
    @classmethod
    def validate_processing_time(cls, v: float) -> float:
        """Ensure processing time is non-negative."""
        if v < 0:
            raise ValueError("Processing time must be non-negative")
        return v
    
    @field_validator("file_size")
    @classmethod
    def validate_file_size(cls, v: int) -> int:
        """Ensure file size is non-negative."""
        if v < 0:
            raise ValueError("File size must be non-negative")
        return v


class ProcessingConfig(BaseModel):
    """Configuration model for markdown processing."""
    
    # Input/Output settings
    input_path: Path = Field(..., description="Input directory path")
    output_path: Path = Field(..., description="Output directory path")
    
    # Numbering configuration
    start_level: int = Field(1, ge=1, le=10, description="Starting level for numbering")
    max_depth: int = Field(6, ge=1, le=10, description="Maximum depth for headline numbering")
    separator: str = Field(".", description="Separator for hierarchical numbers")
    preserve_existing: bool = Field(False, description="Whether to preserve existing numbering")
    
    # File processing settings
    sorting_method: SortingMethod = Field(
        SortingMethod.ALPHABETICAL, 
        description="Method for sorting files within folders"
    )
    filename_separator: str = Field("-", description="Separator between number and filename")
    preserve_original_name: bool = Field(True, description="Whether to preserve original filename")
    include_patterns: List[str] = Field(
        ["*.md", "*.markdown"], 
        description="File patterns to include"
    )
    exclude_patterns: List[str] = Field(
        ["**/.*", "**/*temp*"], 
        description="File patterns to exclude"
    )
    
    # Performance settings
    max_concurrent_files: int = Field(10, ge=1, le=100, description="Maximum concurrent file processing")
    chunk_size: int = Field(8192, ge=1024, le=65536, description="File reading chunk size")
    
    # Logging settings
    log_level: str = Field("INFO", description="Logging level")
    log_format: str = Field("structured", description="Logging format")
    progress_bar: bool = Field(True, description="Whether to show progress bar")
    
    # Validation settings
    validate_output: bool = Field(True, description="Whether to validate output files")
    backup_original: bool = Field(False, description="Whether to backup original files")
    
    @field_validator("input_path", "output_path", mode="before")
    @classmethod
    def validate_paths(cls, v: Any) -> Path:
        """Convert string paths to Path objects."""
        if isinstance(v, str):
            return Path(v)
        return v
    
    @field_validator("separator", "filename_separator")
    @classmethod
    def validate_separators(cls, v: str) -> str:
        """Ensure separators are single characters."""
        if len(v) != 1:
            raise ValueError("Separator must be a single character")
        return v
    
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate logging level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    @field_validator("log_format")
    @classmethod
    def validate_log_format(cls, v: str) -> str:
        """Validate logging format."""
        valid_formats = ["structured", "simple", "json"]
        if v.lower() not in valid_formats:
            raise ValueError(f"Log format must be one of: {valid_formats}")
        return v.lower()
    
    def get_output_timestamp_dir(self) -> Path:
        """Get the timestamped output directory path."""
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return self.output_path / timestamp
    
    def validate_config(self) -> List[str]:
        """Validate the configuration and return any errors."""
        errors = []
        
        # Check if input path exists
        if not self.input_path.exists():
            errors.append(f"Input path does not exist: {self.input_path}")
        
        # Check if input path is a directory
        if not self.input_path.is_dir():
            errors.append(f"Input path is not a directory: {self.input_path}")
        
        # Check if output path can be created
        try:
            self.output_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create output directory: {e}")
        
        # Validate start_level <= max_depth
        if self.start_level > self.max_depth:
            errors.append("start_level cannot be greater than max_depth")
        
        return errors 