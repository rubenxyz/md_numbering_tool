#!/usr/bin/env python3
"""
Simple markdown numbering script.

Usage:
    python main.py input_folder output_folder
    python main.py /path/to/input /path/to/output
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

from src.markdown_numberer.core.models import ProcessingConfig
from src.markdown_numberer.services.processor import AsyncMarkdownProcessor


def create_default_config(input_path: Path, output_path: Path) -> ProcessingConfig:
    """Create a ProcessingConfig with sensible defaults."""
    return ProcessingConfig(
        input_path=input_path,
        output_path=output_path,
        start_level=1,
        max_depth=6,
        separator=".",
        preserve_existing=False,
        sorting_method="alphabetical",
        filename_separator="-",
        preserve_original_name=True,
        include_patterns=["*.md", "*.markdown"],
        exclude_patterns=["**/.*", "**/*temp*"],
        max_concurrent_files=10,
        chunk_size=8192,
        log_level="INFO",
        log_format="structured",
        progress_bar=True,
        validate_output=True,
        backup_original=False
    )


async def process_markdown_files(input_path: Path, output_path: Path, batch_id: Optional[str] = None):
    """Process markdown files with numbering."""
    print(f"Processing markdown files...")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    
    # Create configuration
    config = create_default_config(input_path, output_path)
    
    # Validate configuration
    errors = config.validate_config()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    try:
        # Process files
        async with AsyncMarkdownProcessor(config) as processor:
            stats = await processor.process_directory(
                input_path=input_path,
                output_path=output_path,
                batch_id=batch_id
            )
            
            # Print results
            print(f"\nProcessing complete!")
            print(f"Total files: {stats.total_files}")
            print(f"Processed: {stats.processed_files}")
            print(f"Failed: {stats.failed_files}")
            print(f"Skipped: {stats.skipped_files}")
            print(f"Success rate: {stats.success_rate:.1f}%")
            print(f"Processing time: {stats.processing_duration:.2f} seconds")
            
            if stats.processed_files > 0:
                print(f"Average time per file: {stats.average_processing_time:.3f} seconds")
                print(f"Total headlines processed: {stats.total_headlines}")
            
            return stats.processed_files > 0
            
    except Exception as e:
        print(f"Error processing files: {e}")
        return False


def main():
    """Main entry point."""
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_folder> <output_folder>")
        print("Example: python main.py /path/to/input /path/to/output")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    # Validate input path
    if not input_path.exists():
        print(f"Error: Input path does not exist: {input_path}")
        sys.exit(1)
    
    if not input_path.is_dir():
        print(f"Error: Input path is not a directory: {input_path}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Run the async processing
    success = asyncio.run(process_markdown_files(input_path, output_path))
    
    if success:
        print(f"\n✅ Success! Check the output directory: {output_path}")
        sys.exit(0)
    else:
        print(f"\n❌ Processing failed. Check the logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main() 