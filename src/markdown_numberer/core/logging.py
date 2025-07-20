"""
Structured logging configuration using Loguru.

This module provides centralized logging configuration for the markdown numberer
application, including structured logging formats, log rotation, and output
destinations.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union

from loguru import logger

from .exceptions import LogConfigurationError
from .models import ProcessingConfig


class LoggingConfig:
    """Configuration for structured logging with Loguru."""
    
    def __init__(self, config: ProcessingConfig):
        """Initialize logging configuration.
        
        Args:
            config: Processing configuration containing logging settings
        """
        self.config = config
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Set up Loguru logging configuration."""
        try:
            # Remove default handler
            logger.remove()
            
            # Configure log level
            log_level = self._get_log_level()
            
            # Set up console logging
            self._setup_console_logging(log_level)
            
            # Set up file logging if enabled
            if self.config.log_format == "structured":
                self._setup_file_logging(log_level)
            
            # Set up exception handling
            self._setup_exception_handling()
            
        except Exception as e:
            raise LogConfigurationError(
                f"Failed to configure logging: {e}",
                details={"log_level": self.config.log_level, "log_format": self.config.log_format},
                cause=e
            )
    
    def _get_log_level(self) -> str:
        """Get the appropriate log level from configuration."""
        level_mapping = {
            "DEBUG": "DEBUG",
            "INFO": "INFO", 
            "WARNING": "WARNING",
            "ERROR": "ERROR",
            "CRITICAL": "CRITICAL"
        }
        
        level = self.config.log_level.upper()
        if level not in level_mapping:
            raise LogConfigurationError(
                f"Invalid log level: {level}",
                details={"valid_levels": list(level_mapping.keys())}
            )
        
        return level_mapping[level]
    
    def _get_log_level_from_string(self, level: str) -> str:
        """Get log level from string (for testing purposes).
        
        Args:
            level: Log level string
            
        Returns:
            Mapped log level string
            
        Raises:
            LogConfigurationError: If log level is invalid
        """
        level_mapping = {
            "DEBUG": "DEBUG",
            "INFO": "INFO", 
            "WARNING": "WARNING",
            "ERROR": "ERROR",
            "CRITICAL": "CRITICAL"
        }
        
        if level not in level_mapping:
            raise LogConfigurationError(
                f"Invalid log level: {level}",
                details={"valid_levels": list(level_mapping.keys())}
            )
        
        return level_mapping[level]
    
    def _setup_console_logging(self, log_level: str) -> None:
        """Set up console logging output."""
        if self.config.log_format == "structured":
            # Structured JSON format for console
            format_str = (
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            )
        else:
            # Simple text format for console
            format_str = (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan> | "
                "<level>{message}</level>"
            )
        
        logger.add(
            sys.stdout,
            format=format_str,
            level=log_level,
            colorize=True,
            backtrace=True,
            diagnose=True
        )
    
    def _setup_file_logging(self, log_level: str) -> None:
        """Set up file logging with rotation."""
        try:
            # Create logs directory
            logs_dir = Path(self.config.output_path) / "logs"
            logs_dir.mkdir(parents=True, exist_ok=True)
            
            # Configure log file path
            log_file = logs_dir / "markdown-numberer.log"
            
            # Set up JSON structured logging to file
            logger.add(
                str(log_file),
                format=self._get_json_format(),
                level=log_level,
                rotation="10 MB",
                retention="30 days",
                compression="gz",
                backtrace=True,
                diagnose=True,
                serialize=True  # Enable JSON serialization
            )
            
        except Exception as e:
            raise LogConfigurationError(
                f"Failed to set up file logging: {e}",
                details={"log_file": str(log_file) if 'log_file' in locals() else "unknown"},
                cause=e
            )
    
    def _get_json_format(self) -> str:
        """Get JSON format string for structured logging."""
        return (
            '{"timestamp": "{time:YYYY-MM-DD HH:mm:ss.SSS}", '
            '"level": "{level}", '
            '"logger": "{name}", '
            '"function": "{function}", '
            '"line": {line}, '
            '"message": "{message}"'
            '}'
        )
    
    def _setup_exception_handling(self) -> None:
        """Set up exception handling for unhandled exceptions."""
        def handle_exception(exc_type, exc_value, exc_traceback):
            """Handle unhandled exceptions."""
            if issubclass(exc_type, KeyboardInterrupt):
                # Don't log keyboard interrupts
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            logger.opt(exception=(exc_type, exc_value, exc_traceback)).error(
                "Unhandled exception occurred",
                extra={
                    "exception_type": exc_type.__name__,
                    "exception_message": str(exc_value)
                }
            )
        
        sys.excepthook = handle_exception


def get_logger(name: str) -> "logger":
    """Get a logger instance with the specified name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return logger.bind(name=name)


def log_function_call(func_name: str, **kwargs) -> None:
    """Log a function call with parameters.
    
    Args:
        func_name: Name of the function being called
        **kwargs: Function parameters to log
    """
    logger.debug(
        f"Function call: {func_name}",
        extra={
            "function": func_name,
            "parameters": kwargs
        }
    )


def log_function_result(func_name: str, result: Any, duration: float) -> None:
    """Log a function result and execution time.
    
    Args:
        func_name: Name of the function
        result: Function result (will be truncated if too long)
        duration: Execution time in seconds
    """
    # Truncate result if it's too long
    result_str = str(result)
    if len(result_str) > 200:
        result_str = result_str[:200] + "..."
    
    logger.debug(
        f"Function result: {func_name}",
        extra={
            "function": func_name,
            "result": result_str,
            "duration_seconds": round(duration, 4)
        }
    )


def log_exception(
    logger_instance: "logger",
    exception: Exception,
    context: Optional[Dict[str, Any]] = None,
    level: str = "ERROR"
) -> None:
    """Log an exception with context.
    
    Args:
        logger_instance: Logger instance to use
        exception: Exception to log
        context: Additional context information
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    extra = {
        "exception_type": exception.__class__.__name__,
        "exception_message": str(exception),
    }
    
    if context:
        extra.update(context)
    
    if hasattr(exception, 'details'):
        extra["exception_details"] = exception.details
    
    if hasattr(exception, 'cause'):
        extra["exception_cause"] = {
            "type": exception.cause.__class__.__name__,
            "message": str(exception.cause)
        } if exception.cause else None
    
    # Use the logger instance directly
    log_method = getattr(logger_instance.opt(exception=True), level.lower())
    log_method(
        f"Exception occurred: {exception}",
        extra=extra
    )


def log_processing_event(
    event_type: str,
    file_path: Optional[Union[str, Path]] = None,
    **kwargs
) -> None:
    """Log a processing event.
    
    Args:
        event_type: Type of processing event
        file_path: Path to the file being processed
        **kwargs: Additional event data
    """
    extra = {
        "event_type": event_type,
        "file_path": str(file_path) if file_path else None,
        **kwargs
    }
    
    logger.info(
        f"Processing event: {event_type}",
        extra=extra
    )


def log_performance_metrics(
    operation: str,
    duration: float,
    file_count: Optional[int] = None,
    file_size: Optional[int] = None,
    **kwargs
) -> None:
    """Log performance metrics.
    
    Args:
        operation: Name of the operation
        duration: Duration in seconds
        file_count: Number of files processed
        file_size: Total file size in bytes
        **kwargs: Additional metrics
    """
    extra = {
        "operation": operation,
        "duration_seconds": round(duration, 4),
        "file_count": file_count,
        "file_size_bytes": file_size,
        **kwargs
    }
    
    if file_count and duration:
        extra["files_per_second"] = round(file_count / duration, 2)
    
    if file_size and duration:
        extra["bytes_per_second"] = round(file_size / duration, 2)
    
    logger.info(
        f"Performance metrics: {operation}",
        extra=extra
    ) 