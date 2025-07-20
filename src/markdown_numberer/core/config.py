"""Configuration management for markdown numbering system."""

import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field

from .models import ProcessingConfig, SortingMethod


class NumberingConfig(BaseModel):
    """Configuration for numbering behavior."""
    
    start_level: int = Field(1, ge=1, le=10, description="Starting level for numbering")
    max_depth: int = Field(6, ge=1, le=10, description="Maximum depth for headline numbering")
    separator: str = Field(".", description="Separator for hierarchical numbers")
    preserve_existing: bool = Field(False, description="Whether to preserve existing numbering")


class FileConfig(BaseModel):
    """Configuration for file processing behavior."""
    
    sorting_method: SortingMethod = Field(
        SortingMethod.ALPHABETICAL, 
        description="Method for sorting files within folders"
    )
    filename_separator: str = Field("-", description="Separator between number and filename")
    preserve_original_name: bool = Field(True, description="Whether to preserve original filename")
    include_patterns: list[str] = Field(
        ["*.md", "*.markdown"], 
        description="File patterns to include"
    )
    exclude_patterns: list[str] = Field(
        ["**/.*", "**/*temp*"], 
        description="File patterns to exclude"
    )


class LoggingConfig(BaseModel):
    """Configuration for logging behavior."""
    
    level: str = Field("INFO", description="Logging level")
    format: str = Field("structured", description="Logging format")
    progress_bar: bool = Field(True, description="Whether to show progress bar")


class PerformanceConfig(BaseModel):
    """Configuration for performance settings."""
    
    max_concurrent_files: int = Field(10, ge=1, le=100, description="Maximum concurrent file processing")
    chunk_size: int = Field(8192, ge=1024, le=65536, description="File reading chunk size")


class ValidationConfig(BaseModel):
    """Configuration for validation settings."""
    
    validate_output: bool = Field(True, description="Whether to validate output files")
    backup_original: bool = Field(False, description="Whether to backup original files")


class AppConfig(BaseModel):
    """Complete application configuration."""
    
    numbering: NumberingConfig = Field(default_factory=NumberingConfig)
    files: FileConfig = Field(default_factory=FileConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    validation: ValidationConfig = Field(default_factory=ValidationConfig)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppConfig":
        """Create AppConfig from dictionary."""
        return cls(**data)
    
    @classmethod
    def from_yaml(cls, yaml_path: Union[str, Path]) -> "AppConfig":
        """Load configuration from YAML file."""
        yaml_path = Path(yaml_path)
        
        if not yaml_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {yaml_path}")
        
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        return cls.from_dict(data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self.model_dump()
    
    def to_yaml(self, yaml_path: Union[str, Path]) -> None:
        """Save configuration to YAML file."""
        yaml_path = Path(yaml_path)
        
        # Ensure parent directory exists
        yaml_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use model_dump with mode='json' to properly serialize enums
        data = self.model_dump(mode='json')
        
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, indent=2)
    
    def to_processing_config(self, input_path: Path, output_path: Path) -> ProcessingConfig:
        """Convert AppConfig to ProcessingConfig."""
        return ProcessingConfig(
            input_path=input_path,
            output_path=output_path,
            start_level=self.numbering.start_level,
            max_depth=self.numbering.max_depth,
            separator=self.numbering.separator,
            preserve_existing=self.numbering.preserve_existing,
            sorting_method=self.files.sorting_method,
            filename_separator=self.files.filename_separator,
            preserve_original_name=self.files.preserve_original_name,
            include_patterns=self.files.include_patterns,
            exclude_patterns=self.files.exclude_patterns,
            max_concurrent_files=self.performance.max_concurrent_files,
            chunk_size=self.performance.chunk_size,
            log_level=self.logging.level,
            log_format=self.logging.format,
            progress_bar=self.logging.progress_bar,
            validate_output=self.validation.validate_output,
            backup_original=self.validation.backup_original,
        )


def load_default_config() -> AppConfig:
    """Load default configuration."""
    return AppConfig()


def create_default_config_file(config_path: Union[str, Path]) -> None:
    """Create a default configuration file."""
    config_path = Path(config_path)
    default_config = load_default_config()
    default_config.to_yaml(config_path)


def load_config(config_path: Optional[Union[str, Path]] = None) -> AppConfig:
    """Load configuration from file or return default."""
    if config_path is None:
        return load_default_config()
    
    try:
        return AppConfig.from_yaml(config_path)
    except FileNotFoundError:
        # Return default config if file doesn't exist
        return load_default_config()
    except Exception as e:
        raise ValueError(f"Failed to load configuration from {config_path}: {e}") 