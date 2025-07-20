"""
Custom exception hierarchy for the markdown numberer application.

This module defines a clear hierarchy of custom exceptions tailored to the
application's error scenarios, following Python best practices for naming
and organization.
"""

from typing import Any, Dict, Optional, Union


class MarkdownNumbererError(Exception):
    """Base exception class for all markdown numberer errors.
    
    This is the root exception class that all other exceptions in this
    application should inherit from. It provides a common interface for
    error handling and logging.
    """
    
    def __init__(
        self, 
        message: str, 
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ) -> None:
        """Initialize the exception.
        
        Args:
            message: Human-readable error message
            details: Additional error details for debugging
            cause: The original exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.cause = cause
    
    def __str__(self) -> str:
        """Return string representation of the exception."""
        return self.message
    
    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        details_str = f", details={self.details}" if self.details else ""
        cause_str = f", cause={self.cause}" if self.cause else ""
        return f"{self.__class__.__name__}({self.message}{details_str}{cause_str})"


# Configuration and Setup Errors
class ConfigurationError(MarkdownNumbererError):
    """Base class for configuration-related errors."""
    pass


class InvalidConfigError(ConfigurationError):
    """Raised when configuration is invalid or malformed."""
    pass


class MissingConfigError(ConfigurationError):
    """Raised when required configuration is missing."""
    pass


class ConfigValidationError(ConfigurationError):
    """Raised when configuration validation fails."""
    pass


# File and I/O Errors
class FileOperationError(MarkdownNumbererError):
    """Base class for file operation errors."""
    pass


class FileNotFoundError(FileOperationError):
    """Raised when a required file is not found."""
    pass


class FilePermissionError(FileOperationError):
    """Raised when there are insufficient permissions to access a file."""
    pass


class FileReadError(FileOperationError):
    """Raised when there's an error reading a file."""
    pass


class FileWriteError(FileOperationError):
    """Raised when there's an error writing to a file."""
    pass


class DirectoryNotFoundError(FileOperationError):
    """Raised when a required directory is not found."""
    pass


class DirectoryPermissionError(FileOperationError):
    """Raised when there are insufficient permissions to access a directory."""
    pass


# Markdown Processing Errors
class MarkdownProcessingError(MarkdownNumbererError):
    """Base class for markdown processing errors."""
    pass


class MarkdownParseError(MarkdownProcessingError):
    """Raised when there's an error parsing markdown content."""
    pass


class MarkdownValidationError(MarkdownProcessingError):
    """Raised when markdown content fails validation."""
    pass


class HeadlineProcessingError(MarkdownProcessingError):
    """Raised when there's an error processing headlines."""
    pass


class NumberingError(MarkdownProcessingError):
    """Raised when there's an error in the numbering process."""
    pass


class InvalidHeadlineError(MarkdownProcessingError):
    """Raised when a headline is invalid or malformed."""
    pass


class HeadlineHierarchyError(MarkdownProcessingError):
    """Raised when there's an error in headline hierarchy."""
    pass


# Async Processing Errors
class AsyncProcessingError(MarkdownNumbererError):
    """Base class for async processing errors."""
    pass


class ConcurrencyError(AsyncProcessingError):
    """Raised when there's an error related to concurrent processing."""
    pass


class SemaphoreError(AsyncProcessingError):
    """Raised when there's an error with semaphore management."""
    pass


class TaskCancellationError(AsyncProcessingError):
    """Raised when a processing task is cancelled."""
    pass


# Validation Errors
class ValidationError(MarkdownNumbererError):
    """Base class for validation errors."""
    pass


class InputValidationError(ValidationError):
    """Raised when input validation fails."""
    pass


class OutputValidationError(ValidationError):
    """Raised when output validation fails."""
    pass


class DataValidationError(ValidationError):
    """Raised when data validation fails."""
    pass


# Logging and Monitoring Errors
class LoggingError(MarkdownNumbererError):
    """Base class for logging-related errors."""
    pass


class LogConfigurationError(LoggingError):
    """Raised when there's an error configuring logging."""
    pass


class LogWriteError(LoggingError):
    """Raised when there's an error writing to log files."""
    pass


# Utility Functions
def create_exception_with_context(
    exception_class: type,
    message: str,
    context: Optional[Dict[str, Any]] = None,
    cause: Optional[Exception] = None
) -> MarkdownNumbererError:
    """Create an exception with additional context.
    
    Args:
        exception_class: The exception class to instantiate
        message: The error message
        context: Additional context information
        cause: The original exception that caused this error
        
    Returns:
        An instance of the specified exception class
    """
    if not issubclass(exception_class, MarkdownNumbererError):
        raise ValueError(f"Exception class must inherit from MarkdownNumbererError: {exception_class}")
    
    return exception_class(message, details=context, cause=cause)


def format_exception_details(exception: MarkdownNumbererError) -> Dict[str, Any]:
    """Format exception details for logging or debugging.
    
    Args:
        exception: The exception to format
        
    Returns:
        Dictionary containing formatted exception details
    """
    details = {
        "exception_type": exception.__class__.__name__,
        "message": exception.message,
        "details": exception.details,
    }
    
    if exception.cause:
        details["cause"] = {
            "exception_type": exception.cause.__class__.__name__,
            "message": str(exception.cause),
        }
    
    return details 