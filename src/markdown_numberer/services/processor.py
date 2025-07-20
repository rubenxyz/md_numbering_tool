"""Async file processing engine for high-performance markdown numbering."""

import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Callable, Awaitable
from dataclasses import dataclass, field
from datetime import datetime
import aiofiles
from concurrent.futures import ThreadPoolExecutor

from ..core.models import ProcessingConfig, ProcessingResult, FileNumbering
from ..core.numbering import DefaultNumberingService
from .parser import MarkdownParser
from .headline_processor import HeadlineProcessor
from .io_manager import IOManager


@dataclass
class ProcessingStats:
    """Statistics for file processing operations."""
    total_files: int = 0
    processed_files: int = 0
    skipped_files: int = 0
    failed_files: int = 0
    total_headlines: int = 0
    total_processing_time: float = 0.0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_files == 0:
            return 0.0
        return (self.processed_files / self.total_files) * 100
    
    @property
    def average_processing_time(self) -> float:
        """Calculate average processing time per file."""
        if self.processed_files == 0:
            return 0.0
        return self.total_processing_time / self.processed_files
    
    @property
    def processing_duration(self) -> float:
        """Calculate total processing duration."""
        if not self.start_time or not self.end_time:
            return 0.0
        return (self.end_time - self.start_time).total_seconds()


@dataclass
class ProcessingContext:
    """Context for file processing operations."""
    config: ProcessingConfig
    stats: ProcessingStats = field(default_factory=ProcessingStats)
    processed_files: Set[Path] = field(default_factory=set)
    failed_files: Dict[Path, str] = field(default_factory=dict)
    numbering_service: Optional[DefaultNumberingService] = None
    parser: Optional[MarkdownParser] = None
    executor: Optional[ThreadPoolExecutor] = None


class AsyncMarkdownProcessor:
    """Async processor for markdown files with concurrent processing capabilities."""
    
    def __init__(self, config: ProcessingConfig):
        """Initialize the async processor with configuration."""
        self.config = config
        self.numbering_service = DefaultNumberingService(config)
        self.headline_processor = HeadlineProcessor(config)
        self.parser = MarkdownParser(config)
        self.io_manager = IOManager(config)
        self.logger = logging.getLogger(__name__)
        self._semaphore: Optional[asyncio.Semaphore] = None
        self._executor: Optional[ThreadPoolExecutor] = None
        
    async def __aenter__(self):
        """Async context manager entry."""
        await self._initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self._cleanup()
    
    async def _initialize(self):
        """Initialize async resources."""
        # Create semaphore for concurrent file processing
        self._semaphore = asyncio.Semaphore(self.config.max_concurrent_files)
        
        # Create thread pool executor for I/O operations
        self._executor = ThreadPoolExecutor(
            max_workers=self.config.max_concurrent_files,
            thread_name_prefix="markdown_processor"
        )
        
        self.logger.info(f"Initialized async processor with {self.config.max_concurrent_files} concurrent workers")
    
    async def _cleanup(self):
        """Clean up async resources."""
        if self._executor:
            self._executor.shutdown(wait=True)
            self._executor = None
        
        self.logger.info("Cleaned up async processor resources")
    
    async def process_directory(self, input_path: Path, output_path: Path, batch_id: Optional[str] = None) -> ProcessingStats:
        """Process all markdown files in a directory asynchronously.
        
        Args:
            input_path: Input directory path
            output_path: Output directory path
            batch_id: Optional custom batch ID for timestamped output
            
        Returns:
            ProcessingStats with processing results
        """
        stats = ProcessingStats(start_time=datetime.now())
        
        try:
            # Start batch processing with IOManager
            batch_metadata = self.io_manager.start_batch(input_path, batch_id)
            timestamped_output_path = batch_metadata.output_path
            
            # Discover markdown files
            files = await self._discover_files(input_path)
            stats.total_files = len(files)
            
            self.logger.info(f"Discovered {stats.total_files} markdown files for processing")
            self.logger.info(f"Using timestamped output directory: {timestamped_output_path}")
            
            # Process files concurrently
            tasks = [
                self._process_file_with_semaphore(file_path, timestamped_output_path, stats)
                for file_path in files
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Update stats from results and add file mappings
            for result in results:
                if isinstance(result, ProcessingResult):
                    # Add file mapping to IOManager
                    self.io_manager.add_file_mapping(result)
                    
                    if result.success:
                        stats.processed_files += 1
                        stats.total_headlines += result.headline_count
                        stats.total_processing_time += result.processing_time
                    else:
                        stats.failed_files += 1
                        if result.error_message:
                            self.logger.error(f"File processing failed: {result.error_message}")
                elif isinstance(result, Exception):
                    stats.failed_files += 1
                    self.logger.error(f"Unexpected error: {result}")
            
            stats.skipped_files = stats.total_files - stats.processed_files - stats.failed_files
            
            # End batch processing and generate reports
            stats_dict = {
                'total_files': stats.total_files,
                'processed_files': stats.processed_files,
                'failed_files': stats.failed_files,
                'skipped_files': stats.skipped_files,
                'total_headlines': stats.total_headlines,
                'total_processing_time': stats.total_processing_time,
                'average_processing_time': stats.average_processing_time
            }
            self.io_manager.end_batch(stats_dict)
            
        except Exception as e:
            self.logger.error(f"Directory processing failed: {e}")
            raise
        finally:
            stats.end_time = datetime.now()
            self._log_processing_summary(stats)
        
        return stats
    
    async def _discover_files(self, input_path: Path) -> List[Path]:
        """Discover markdown files based on configuration patterns.
        
        Args:
            input_path: Input directory path
            
        Returns:
            List of markdown file paths
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input path does not exist: {input_path}")
        
        if not input_path.is_dir():
            raise ValueError(f"Input path is not a directory: {input_path}")
        
        files = []
        
        # Use thread pool for file system operations
        loop = asyncio.get_event_loop()
        
        for pattern in self.config.include_patterns:
            pattern_files = await loop.run_in_executor(
                self._executor,
                lambda: list(input_path.rglob(pattern))
            )
            files.extend(pattern_files)
        
        # Apply exclude patterns
        excluded_files = set()
        for pattern in self.config.exclude_patterns:
            pattern_files = await loop.run_in_executor(
                self._executor,
                lambda: list(input_path.rglob(pattern))
            )
            excluded_files.update(pattern_files)
        
        # Filter out excluded files and non-files
        files = [
            f for f in files 
            if f.is_file() and f not in excluded_files
        ]
        
        # Sort files based on configuration
        files = await self._sort_files(files)
        
        return files
    
    async def _sort_files(self, files: List[Path]) -> List[Path]:
        """Sort files based on configuration sorting method.
        
        Args:
            files: List of file paths to sort
            
        Returns:
            Sorted list of file paths
        """
        if not files:
            return files
        
        # Use thread pool for sorting operations
        loop = asyncio.get_event_loop()
        
        if self.config.sorting_method.value == "alphabetical":
            return await loop.run_in_executor(
                self._executor,
                lambda: sorted(files, key=lambda f: f.name.lower())
            )
        elif self.config.sorting_method.value == "creation_date":
            return await loop.run_in_executor(
                self._executor,
                lambda: sorted(files, key=lambda f: f.stat().st_ctime)
            )
        elif self.config.sorting_method.value == "modification_date":
            return await loop.run_in_executor(
                self._executor,
                lambda: sorted(files, key=lambda f: f.stat().st_mtime)
            )
        elif self.config.sorting_method.value == "size":
            return await loop.run_in_executor(
                self._executor,
                lambda: sorted(files, key=lambda f: f.stat().st_size)
            )
        else:
            # Default to alphabetical
            return await loop.run_in_executor(
                self._executor,
                lambda: sorted(files, key=lambda f: f.name.lower())
            )
    
    async def _process_file_with_semaphore(
        self, 
        file_path: Path, 
        output_path: Path, 
        stats: ProcessingStats
    ) -> ProcessingResult:
        """Process a single file with semaphore control.
        
        Args:
            file_path: Input file path
            output_path: Output directory path
            stats: Processing statistics
            
        Returns:
            ProcessingResult for the file
        """
        async with self._semaphore:
            return await self._process_single_file(file_path, output_path)
    
    async def _process_single_file(self, file_path: Path, output_path: Path) -> ProcessingResult:
        """Process a single markdown file asynchronously.
        
        Args:
            file_path: Input file path
            output_path: Output directory path
            
        Returns:
            ProcessingResult for the file
        """
        start_time = datetime.now()
        
        try:
            # Create numbering service and parser
            numbering_service = DefaultNumberingService(self.config)
            parser = MarkdownParser(self.config)
            
            # Get preserved output path using IOManager
            preserved_output_path = self.io_manager.get_output_path_for_file(file_path)
            
            # Create file numbering with preserved structure
            file_numbering = numbering_service.create_file_numbering(file_path, preserved_output_path.parent)
            
            # Read file content asynchronously
            content = await self._read_file_async(file_path)
            
            # Process headlines in the content
            headline_result = self.headline_processor.process_headlines(content, file_numbering)
            processed_content = headline_result.processed_content
            headline_count = headline_result.headline_count
            
            # Write processed content asynchronously
            output_file = file_numbering.numbered_path
            await self._write_file_async(output_file, processed_content)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return ProcessingResult(
                file_numbering=file_numbering,
                success=True,
                processing_time=processing_time,
                file_size=len(content),
                headline_count=headline_count,
                content_modified=True
            )
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Failed to process {file_path}: {e}")
            
            # Create a minimal FileNumbering for failed results
            failed_numbering = FileNumbering(
                original_path=file_path,
                numbered_path=Path(""),
                file_number="",
                folder_number="",
                original_name=file_path.stem,
                extension=file_path.suffix
            )
            
            return ProcessingResult(
                file_numbering=failed_numbering,
                success=False,
                error_message=str(e),
                processing_time=processing_time,
                file_size=0,
                headline_count=0,
                content_modified=False
            )
    
    async def _read_file_async(self, file_path: Path) -> str:
        """Read file content asynchronously with encoding fallback.
        
        Args:
            file_path: File path to read
            
        Returns:
            File content as string
        """
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                return await f.read()
        except UnicodeDecodeError:
            # Fallback to latin-1 encoding
            async with aiofiles.open(file_path, 'r', encoding='latin-1') as f:
                return await f.read()
    
    async def _write_file_async(self, file_path: Path, content: str):
        """Write content to file asynchronously.
        
        Args:
            file_path: File path to write
            content: Content to write
        """
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(content)
    
    def _log_processing_summary(self, stats: ProcessingStats):
        """Log processing summary statistics.
        
        Args:
            stats: Processing statistics
        """
        self.logger.info("Processing Summary:")
        self.logger.info(f"  Total files: {stats.total_files}")
        self.logger.info(f"  Processed: {stats.processed_files}")
        self.logger.info(f"  Skipped: {stats.skipped_files}")
        self.logger.info(f"  Failed: {stats.failed_files}")
        self.logger.info(f"  Success rate: {stats.success_rate:.1f}%")
        self.logger.info(f"  Total headlines: {stats.total_headlines}")
        self.logger.info(f"  Total processing time: {stats.total_processing_time:.2f}s")
        self.logger.info(f"  Average processing time: {stats.average_processing_time:.2f}s")
        self.logger.info(f"  Processing duration: {stats.processing_duration:.2f}s")
    
    async def process_single_file(self, file_path: Path, output_path: Path) -> ProcessingResult:
        """Process a single file without directory discovery.
        
        Args:
            file_path: Input file path
            output_path: Output directory path
            
        Returns:
            ProcessingResult for the file
        """
        return await self._process_single_file(file_path, output_path)
    
    async def validate_processing_config(self) -> List[str]:
        """Validate the processing configuration.
        
        Returns:
            List of validation error messages
        """
        errors = []
        
        # Validate input path
        if not self.config.input_path or str(self.config.input_path).strip() == "":
            errors.append("Input path is required")
        
        # Validate output path
        if not self.config.output_path or str(self.config.output_path).strip() == "":
            errors.append("Output path is required")
        
        # Validate concurrent file limit
        if self.config.max_concurrent_files <= 0:
            errors.append("Max concurrent files must be positive")
        
        # Validate chunk size
        if self.config.chunk_size <= 0:
            errors.append("Chunk size must be positive")
        
        return errors
    
    async def get_processing_estimate(self, input_path: Path) -> Dict[str, Any]:
        """Get processing time and resource estimates.
        
        Args:
            input_path: Input directory path
            
        Returns:
            Dictionary with processing estimates
        """
        try:
            files = await self._discover_files(input_path)
            
            # Estimate based on file count and average processing time
            estimated_time = len(files) * 0.1  # Rough estimate: 0.1s per file
            estimated_memory = len(files) * 1024 * 1024  # Rough estimate: 1MB per file
            
            return {
                'file_count': len(files),
                'estimated_processing_time': estimated_time,
                'estimated_memory_usage': estimated_memory,
                'concurrent_workers': self.config.max_concurrent_files,
                'chunk_size': self.config.chunk_size
            }
        except Exception as e:
            return {
                'error': str(e),
                'file_count': 0,
                'estimated_processing_time': 0,
                'estimated_memory_usage': 0
            } 