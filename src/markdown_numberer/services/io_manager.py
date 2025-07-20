"""I/O management service for batch processing with timestamped output."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import shutil
from dataclasses import dataclass, asdict
import time
import traceback

from ..core.models import ProcessingConfig, FileNumbering, ProcessingResult
from ..core.exceptions import FileOperationError


@dataclass
class BatchMetadata:
    """Metadata for a batch processing run."""
    batch_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    input_path: Optional[Path] = None
    output_path: Optional[Path] = None
    config_snapshot: Optional[Dict[str, Any]] = None
    total_files: int = 0
    processed_files: int = 0
    failed_files: int = 0
    skipped_files: int = 0
    total_processing_time: float = 0.0
    average_processing_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        # Convert datetime objects to strings
        if data['start_time']:
            data['start_time'] = data['start_time'].isoformat()
        if data['end_time']:
            data['end_time'] = data['end_time'].isoformat()
        # Convert Path objects to strings
        if data['input_path']:
            data['input_path'] = str(data['input_path'])
        if data['output_path']:
            data['output_path'] = str(data['output_path'])
        return data


@dataclass
class FileMapping:
    """Mapping between input and output files."""
    input_path: Path
    output_path: Path
    file_number: str
    folder_number: str
    original_name: str
    extension: str
    success: bool
    processing_time: float
    file_size: int
    headline_count: int
    content_modified: bool
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        # Convert Path objects to strings
        data['input_path'] = str(data['input_path'])
        data['output_path'] = str(data['output_path'])
        return data


class ProcessingLogger:
    """Handles detailed processing log generation."""
    
    def __init__(self, log_dir: Path):
        """Initialize the processing logger.
        
        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up different log files
        self.setup_loggers()
    
    def setup_loggers(self):
        """Set up different loggers for different types of logs."""
        # Main processing log
        self.processing_logger = self._setup_logger(
            'processing', 
            self.log_dir / 'processing.log',
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Error log
        self.error_logger = self._setup_logger(
            'errors',
            self.log_dir / 'errors.log',
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Performance log
        self.performance_logger = self._setup_logger(
            'performance',
            self.log_dir / 'performance.log',
            '%(asctime)s - %(message)s'
        )
        
        # Batch log
        self.batch_logger = self._setup_logger(
            'batch',
            self.log_dir / 'batch.log',
            '%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def _setup_logger(self, name: str, log_file: Path, format_string: str) -> logging.Logger:
        """Set up a logger with file handler.
        
        Args:
            name: Logger name
            log_file: Log file path
            format_string: Log format string
            
        Returns:
            Configured logger
        """
        logger = logging.getLogger(f'markdown_numberer.{name}')
        logger.setLevel(logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Create file handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(format_string)
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(file_handler)
        
        return logger
    
    def log_batch_start(self, batch_id: str, input_path: Path, output_path: Path, config: ProcessingConfig):
        """Log batch processing start.
        
        Args:
            batch_id: Batch identifier
            input_path: Input directory path
            output_path: Output directory path
            config: Processing configuration
        """
        self.batch_logger.info(f"=== BATCH START: {batch_id} ===")
        self.batch_logger.info(f"Input Path: {input_path}")
        self.batch_logger.info(f"Output Path: {output_path}")
        self.batch_logger.info(f"Configuration: {config.model_dump()}")
        self.batch_logger.info("=" * 50)
    
    def log_batch_end(self, batch_id: str, metadata: BatchMetadata):
        """Log batch processing end.
        
        Args:
            batch_id: Batch identifier
            metadata: Batch metadata
        """
        self.batch_logger.info(f"=== BATCH END: {batch_id} ===")
        self.batch_logger.info(f"Total Files: {metadata.total_files}")
        self.batch_logger.info(f"Processed Files: {metadata.processed_files}")
        self.batch_logger.info(f"Failed Files: {metadata.failed_files}")
        self.batch_logger.info(f"Skipped Files: {metadata.skipped_files}")
        self.batch_logger.info(f"Total Processing Time: {metadata.total_processing_time:.2f}s")
        self.batch_logger.info(f"Average Processing Time: {metadata.average_processing_time:.2f}s")
        self.batch_logger.info("=" * 50)
    
    def log_file_processing_start(self, file_path: Path, file_size: int):
        """Log start of file processing.
        
        Args:
            file_path: File being processed
            file_size: File size in bytes
        """
        self.processing_logger.info(f"Processing file: {file_path} (size: {file_size} bytes)")
    
    def log_file_processing_success(self, file_path: Path, result: ProcessingResult):
        """Log successful file processing.
        
        Args:
            file_path: File that was processed
            result: Processing result
        """
        self.processing_logger.info(
            f"✓ Successfully processed: {file_path} -> {result.file_numbering.numbered_path} "
            f"(headlines: {result.headline_count}, time: {result.processing_time:.2f}s)"
        )
        
        # Log performance metrics
        self.performance_logger.info(
            f"FILE_SUCCESS|{file_path}|{result.file_numbering.numbered_path}|"
            f"{result.processing_time:.3f}|{result.file_size}|{result.headline_count}"
        )
    
    def log_file_processing_error(self, file_path: Path, error: Exception, processing_time: float):
        """Log file processing error.
        
        Args:
            file_path: File that failed to process
            error: Exception that occurred
            processing_time: Time spent before error
        """
        error_msg = f"✗ Failed to process: {file_path} (time: {processing_time:.2f}s)"
        self.processing_logger.error(error_msg)
        self.error_logger.error(f"File: {file_path}")
        self.error_logger.error(f"Error: {str(error)}")
        self.error_logger.error(f"Traceback: {traceback.format_exc()}")
        self.error_logger.error("-" * 40)
        
        # Log performance metrics
        self.performance_logger.info(
            f"FILE_ERROR|{file_path}|ERROR|{processing_time:.3f}|0|0"
        )
    
    def log_file_skipped(self, file_path: Path, reason: str):
        """Log file being skipped.
        
        Args:
            file_path: File being skipped
            reason: Reason for skipping
        """
        self.processing_logger.info(f"⏭ Skipped: {file_path} (reason: {reason})")
    
    def log_performance_metrics(self, batch_id: str, total_files: int, total_time: float, 
                               avg_time: float, success_rate: float):
        """Log batch performance metrics.
        
        Args:
            batch_id: Batch identifier
            total_files: Total number of files
            total_time: Total processing time
            avg_time: Average processing time per file
            success_rate: Success rate percentage
        """
        self.performance_logger.info(
            f"BATCH_METRICS|{batch_id}|{total_files}|{total_time:.3f}|"
            f"{avg_time:.3f}|{success_rate:.1f}%"
        )
    
    def log_configuration_change(self, old_config: ProcessingConfig, new_config: ProcessingConfig):
        """Log configuration changes.
        
        Args:
            old_config: Previous configuration
            new_config: New configuration
        """
        self.batch_logger.info("Configuration changed:")
        old_dict = old_config.model_dump()
        new_dict = new_config.model_dump()
        
        for key in old_dict:
            if old_dict[key] != new_dict[key]:
                self.batch_logger.info(f"  {key}: {old_dict[key]} -> {new_dict[key]}")
    
    def generate_processing_summary(self, batch_id: str, metadata: BatchMetadata, 
                                  file_mappings: List[FileMapping]) -> str:
        """Generate a detailed processing summary.
        
        Args:
            batch_id: Batch identifier
            metadata: Batch metadata
            file_mappings: List of file mappings
            
        Returns:
            Formatted summary string
        """
        summary = f"""# Processing Summary for Batch: {batch_id}

## Batch Statistics
- **Start Time**: {metadata.start_time.strftime('%Y-%m-%d %H:%M:%S')}
- **End Time**: {metadata.end_time.strftime('%Y-%m-%d %H:%M:%S') if metadata.end_time else 'Not completed'}
- **Duration**: {metadata.total_processing_time:.2f} seconds
- **Total Files**: {metadata.total_files}
- **Processed Files**: {metadata.processed_files}
- **Failed Files**: {metadata.failed_files}
- **Skipped Files**: {metadata.skipped_files}
- **Success Rate**: {(metadata.processed_files / metadata.total_files * 100) if metadata.total_files > 0 else 0:.1f}%
- **Average Processing Time**: {metadata.average_processing_time:.2f} seconds per file

## File Processing Details
"""
        
        # Group files by status
        successful_files = [m for m in file_mappings if m.success]
        failed_files = [m for m in file_mappings if not m.success]
        
        if successful_files:
            summary += "\n### Successfully Processed Files\n"
            for mapping in successful_files:
                summary += f"- `{mapping.input_path}` → `{mapping.output_path}` "
                summary += f"(headlines: {mapping.headline_count}, time: {mapping.processing_time:.2f}s)\n"
        
        if failed_files:
            summary += "\n### Failed Files\n"
            for mapping in failed_files:
                summary += f"- `{mapping.input_path}`: {mapping.error_message or 'Unknown error'}\n"
        
        summary += "\n## Performance Analysis\n"
        if successful_files:
            processing_times = [m.processing_time for m in successful_files]
            file_sizes = [m.file_size for m in successful_files]
            headline_counts = [m.headline_count for m in successful_files]
            
            summary += f"- **Fastest File**: {min(processing_times):.2f}s\n"
            summary += f"- **Slowest File**: {max(processing_times):.2f}s\n"
            summary += f"- **Largest File**: {max(file_sizes)} bytes\n"
            summary += f"- **Most Headlines**: {max(headline_counts)}\n"
            summary += f"- **Average File Size**: {sum(file_sizes) / len(file_sizes):.0f} bytes\n"
        
        return summary


class IOManager:
    """Manages I/O operations for batch processing with comprehensive logging."""
    
    def __init__(self, config: ProcessingConfig):
        """Initialize the I/O manager.
        
        Args:
            config: Processing configuration
        """
        self.config = config
        self.batch_metadata: Optional[BatchMetadata] = None
        self.file_mappings: List[FileMapping] = []
        self.output_dir: Optional[Path] = None
        self.logger = logging.getLogger(__name__)
        self.processing_logger: Optional[ProcessingLogger] = None
    
    def create_timestamped_output_directory(self, batch_id: Optional[str] = None) -> Path:
        """Create a timestamped output directory for batch processing.
        
        Args:
            batch_id: Optional custom batch ID
            
        Returns:
            Path to the created output directory
        """
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        if batch_id:
            dir_name = batch_id
        else:
            dir_name = timestamp
        
        output_dir = self.config.output_path / dir_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.output_dir = output_dir
        self.logger.info(f"Created timestamped output directory: {output_dir}")
        
        return output_dir
    
    def preserve_folder_structure(self, input_path: Path, output_dir: Path) -> Path:
        """Preserve the folder structure from input to output.
        
        Args:
            input_path: Input file path
            output_dir: Base output directory
            
        Returns:
            Path to the preserved folder structure in output
        """
        # Get relative path from input base to the file
        try:
            relative_path = input_path.relative_to(self.config.input_path)
        except ValueError:
            # If input_path is not relative to input base, use just the filename
            relative_path = Path(input_path.name)
        
        # Create the preserved structure in output
        preserved_path = output_dir / relative_path.parent
        preserved_path.mkdir(parents=True, exist_ok=True)
        
        return preserved_path
    
    def create_output_subdirectories(self, output_dir: Path) -> List[str]:
        """Create standard output subdirectories.
        
        Args:
            output_dir: Base output directory
            
        Returns:
            List of created subdirectory names
        """
        subdirs = ['logs', 'mappings', 'reports']
        
        if self.config.backup_original:
            subdirs.append('backups')
        
        for subdir_name in subdirs:
            subdir_path = output_dir / subdir_name
            subdir_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize processing logger
        self.processing_logger = ProcessingLogger(output_dir / 'logs')
        
        return subdirs
    
    def start_batch(self, input_path: Path, batch_id: Optional[str] = None) -> BatchMetadata:
        """Start a new batch processing run.
        
        Args:
            input_path: Input directory path
            batch_id: Optional custom batch ID
            
        Returns:
            BatchMetadata for the new batch
        """
        # Create timestamped output directory
        output_dir = self.create_timestamped_output_directory(batch_id)
        
        # Create subdirectories
        subdirs = self.create_output_subdirectories(output_dir)
        
        # Convert config to dict with string paths for JSON serialization
        config_dict = self.config.model_dump()
        config_dict['input_path'] = str(config_dict['input_path'])
        config_dict['output_path'] = str(config_dict['output_path'])
        
        # Initialize batch metadata
        self.batch_metadata = BatchMetadata(
            batch_id=batch_id or datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
            start_time=datetime.now(),
            input_path=input_path,
            output_path=output_dir,
            config_snapshot=config_dict
        )
        
        # Log batch start
        if self.processing_logger:
            self.processing_logger.log_batch_start(
                self.batch_metadata.batch_id, input_path, output_dir, self.config
            )
        
        # Save batch metadata
        self._save_batch_metadata()
        
        self.logger.info(f"Started batch processing: {self.batch_metadata.batch_id}")
        return self.batch_metadata
    
    def add_file_mapping(self, result: ProcessingResult) -> None:
        """Add a file mapping from processing result.
        
        Args:
            result: Processing result containing file information
        """
        mapping = FileMapping(
            input_path=result.file_numbering.original_path,
            output_path=result.file_numbering.numbered_path,
            file_number=result.file_numbering.file_number,
            folder_number=result.file_numbering.folder_number,
            original_name=result.file_numbering.original_name,
            extension=result.file_numbering.extension,
            success=result.success,
            processing_time=result.processing_time,
            file_size=result.file_size,
            headline_count=result.headline_count,
            content_modified=result.content_modified,
            error_message=result.error_message
        )
        
        self.file_mappings.append(mapping)
        
        # Log file processing result
        if self.processing_logger:
            if result.success:
                self.processing_logger.log_file_processing_success(
                    result.file_numbering.original_path, result
                )
            else:
                self.processing_logger.log_file_processing_error(
                    result.file_numbering.original_path, 
                    Exception(result.error_message or "Unknown error"),
                    result.processing_time
                )
    
    def end_batch(self, stats: Optional[Dict[str, Any]] = None) -> BatchMetadata:
        """End the current batch processing run.
        
        Args:
            stats: Optional processing statistics
            
        Returns:
            Updated BatchMetadata
        """
        if not self.batch_metadata:
            raise RuntimeError("No active batch to end")
        
        # Update batch metadata with end time and stats
        self.batch_metadata.end_time = datetime.now()
        
        if stats:
            self.batch_metadata.total_files = stats.get('total_files', 0)
            self.batch_metadata.processed_files = stats.get('processed_files', 0)
            self.batch_metadata.failed_files = stats.get('failed_files', 0)
            self.batch_metadata.skipped_files = stats.get('skipped_files', 0)
            self.batch_metadata.total_processing_time = stats.get('total_processing_time', 0.0)
            self.batch_metadata.average_processing_time = stats.get('average_processing_time', 0.0)
        
        # Log batch end
        if self.processing_logger:
            self.processing_logger.log_batch_end(self.batch_metadata.batch_id, self.batch_metadata)
            
            # Log performance metrics
            if self.batch_metadata.total_files > 0:
                success_rate = (self.batch_metadata.processed_files / self.batch_metadata.total_files) * 100
                self.processing_logger.log_performance_metrics(
                    self.batch_metadata.batch_id,
                    self.batch_metadata.total_files,
                    self.batch_metadata.total_processing_time,
                    self.batch_metadata.average_processing_time,
                    success_rate
                )
        
        # Generate reports
        self._generate_file_mapping_report()
        self._generate_summary_report(stats or {})
        
        # Save final batch metadata
        self._save_batch_metadata()
        
        self.logger.info(f"Completed batch processing: {self.batch_metadata.batch_id}")
        return self.batch_metadata
    
    def _save_batch_metadata(self) -> None:
        """Save batch metadata to JSON file."""
        if not self.batch_metadata or not self.output_dir:
            return
        
        metadata_file = self.output_dir / 'batch_metadata.json'
        try:
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.batch_metadata.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save batch metadata: {e}")
            raise FileOperationError(f"Failed to save batch metadata: {e}")
    
    def _generate_file_mapping_report(self) -> None:
        """Generate file mapping report in JSON format."""
        if not self.output_dir:
            return
        
        mapping_file = self.output_dir / 'mappings' / 'file_mappings.json'
        try:
            # Ensure mappings directory exists
            mapping_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert file mappings to dictionaries
            mappings_data = [mapping.to_dict() for mapping in self.file_mappings]
            
            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump(mappings_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Generated file mapping report: {mapping_file}")
        except Exception as e:
            self.logger.error(f"Failed to generate file mapping report: {e}")
            raise FileOperationError(f"Failed to generate file mapping report: {e}")
    
    def _generate_summary_report(self, stats: Dict[str, Any]) -> None:
        """Generate summary report in Markdown format."""
        if not self.batch_metadata or not self.output_dir:
            return
        
        report_file = self.output_dir / 'reports' / 'summary_report.md'
        try:
            # Ensure reports directory exists
            report_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Calculate duration if end_time is available
            if self.batch_metadata.end_time:
                duration = (self.batch_metadata.end_time - self.batch_metadata.start_time).total_seconds()
                end_time_str = self.batch_metadata.end_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                duration = 0.0
                end_time_str = "Not completed"
            
            success_rate = (self.batch_metadata.processed_files / self.batch_metadata.total_files * 100) if self.batch_metadata.total_files > 0 else 0
            
            report_content = f"""# Batch Processing Summary Report

## Batch Information
- **Batch ID**: {self.batch_metadata.batch_id}
- **Start Time**: {self.batch_metadata.start_time.strftime('%Y-%m-%d %H:%M:%S')}
- **End Time**: {end_time_str}
- **Duration**: {duration:.2f} seconds

## Processing Statistics
- **Total Files**: {self.batch_metadata.total_files}
- **Processed Files**: {self.batch_metadata.processed_files}
- **Failed Files**: {self.batch_metadata.failed_files}
- **Skipped Files**: {self.batch_metadata.skipped_files}
- **Success Rate**: {success_rate:.1f}%

## Configuration
- **Input Path**: {self.batch_metadata.input_path}
- **Output Path**: {self.batch_metadata.output_path}
- **Start Level**: {self.config.start_level}
- **Max Depth**: {self.config.max_depth}
- **Separator**: {self.config.separator}
- **Preserve Existing**: {self.config.preserve_existing}

## File Processing Details
- **Total Headlines**: {stats.get('total_headlines', 0)}
- **Total Processing Time**: {stats.get('total_processing_time', 0):.2f} seconds
- **Average Processing Time**: {stats.get('average_processing_time', 0):.2f} seconds per file

## Output Structure
- **Batch Directory**: {self.output_dir}
- **File Mappings**: `mappings/file_mappings.json`
- **Batch Metadata**: `batch_metadata.json`
- **Processing Logs**: `logs/` directory

## Notes
- All processed files maintain their original folder structure
- Failed files are logged with error details
- File mappings provide input-to-output path relationships
"""
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            self.logger.info(f"Generated summary report: {report_file}")
        except Exception as e:
            self.logger.error(f"Failed to generate summary report: {e}")
            raise FileOperationError(f"Failed to generate summary report: {e}")
    
    def get_output_path_for_file(self, input_file: Path) -> Path:
        """Get the output path for a given input file, preserving folder structure.
        
        Args:
            input_file: Input file path
            
        Returns:
            Output file path with preserved structure
        """
        if not self.output_dir:
            raise RuntimeError("No active batch")
        
        # Preserve folder structure
        preserved_dir = self.preserve_folder_structure(input_file, self.output_dir)
        
        # Create output filename
        if self.config.preserve_original_name:
            output_filename = input_file.name
        else:
            # This will be updated by the numbering service
            output_filename = input_file.name
        
        return preserved_dir / output_filename
    
    def log_file_processing_start(self, file_path: Path, file_size: int) -> None:
        """Log the start of file processing.
        
        Args:
            file_path: File being processed
            file_size: File size in bytes
        """
        if self.processing_logger:
            self.processing_logger.log_file_processing_start(file_path, file_size)
    
    def log_file_skipped(self, file_path: Path, reason: str) -> None:
        """Log a file being skipped.
        
        Args:
            file_path: File being skipped
            reason: Reason for skipping
        """
        if self.processing_logger:
            self.processing_logger.log_file_skipped(file_path, reason)
    
    def generate_detailed_summary(self) -> str:
        """Generate a detailed processing summary.
        
        Returns:
            Detailed summary string
        """
        if not self.batch_metadata or not self.processing_logger:
            return "No batch data available"
        
        return self.processing_logger.generate_processing_summary(
            self.batch_metadata.batch_id,
            self.batch_metadata,
            self.file_mappings
        ) 