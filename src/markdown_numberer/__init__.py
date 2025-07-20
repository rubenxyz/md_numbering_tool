"""Modern tool for hierarchical numbering of markdown files and headlines."""

__version__ = "1.0.0"
__author__ = "Ruben"
__email__ = "ruben@example.com"

from .core.models import ProcessingConfig, FileNumbering, ProcessingResult, SortingMethod
from .core.config import AppConfig, NumberingConfig, FileConfig

__all__ = [
    "ProcessingConfig",
    "FileNumbering", 
    "ProcessingResult",
    "SortingMethod",
    "AppConfig",
    "NumberingConfig",
    "FileConfig",
] 