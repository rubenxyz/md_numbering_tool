"""File mapping service for tracking input-to-output file relationships."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib

from ..core.models import ProcessingResult, FileNumbering
from ..core.exceptions import FileOperationError


@dataclass
class FileMappingEntry:
    """Detailed file mapping entry with metadata."""
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
    input_hash: Optional[str] = None
    output_hash: Optional[str] = None
    mapping_id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        # Convert Path objects to strings
        data['input_path'] = str(data['input_path'])
        data['output_path'] = str(data['output_path'])
        # Convert datetime to string
        if data['created_at']:
            data['created_at'] = data['created_at'].isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FileMappingEntry':
        """Create FileMappingEntry from dictionary."""
        # Convert string paths back to Path objects
        data['input_path'] = Path(data['input_path'])
        data['output_path'] = Path(data['output_path'])
        # Convert string datetime back to datetime object
        if data.get('created_at'):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)


class FileMapper:
    """Manages input-to-output file mappings with comprehensive tracking."""
    
    def __init__(self, output_dir: Path):
        """Initialize the file mapper.
        
        Args:
            output_dir: Output directory for storing mapping files
        """
        self.output_dir = output_dir
        self.mappings_dir = output_dir / 'mappings'
        self.mappings_dir.mkdir(parents=True, exist_ok=True)
        
        self.mappings: Dict[str, FileMappingEntry] = {}
        self.input_to_output: Dict[Path, Path] = {}
        self.output_to_input: Dict[Path, Path] = {}
        self.file_number_to_path: Dict[str, Path] = {}
        self.logger = logging.getLogger(__name__)
        
        # Load existing mappings if they exist
        self._load_existing_mappings()
    
    def _load_existing_mappings(self) -> None:
        """Load existing mappings from disk."""
        mapping_file = self.mappings_dir / 'file_mappings.json'
        if mapping_file.exists():
            try:
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data:
                    mapping = FileMappingEntry.from_dict(item)
                    self._add_mapping_to_indexes(mapping)
                
                self.logger.info(f"Loaded {len(data)} existing file mappings")
            except Exception as e:
                self.logger.warning(f"Failed to load existing mappings: {e}")
    
    def _add_mapping_to_indexes(self, mapping: FileMappingEntry) -> None:
        """Add mapping to all internal indexes.
        
        Args:
            mapping: File mapping entry to add
        """
        mapping_id = mapping.mapping_id or self._generate_mapping_id(mapping)
        mapping.mapping_id = mapping_id
        
        self.mappings[mapping_id] = mapping
        self.input_to_output[mapping.input_path] = mapping.output_path
        self.output_to_input[mapping.output_path] = mapping.input_path
        
        if mapping.file_number:
            self.file_number_to_path[mapping.file_number] = mapping.output_path
    
    def _generate_mapping_id(self, mapping: FileMappingEntry) -> str:
        """Generate a unique mapping ID.
        
        Args:
            mapping: File mapping entry
            
        Returns:
            Unique mapping ID
        """
        # Use input path and timestamp to generate unique ID
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        path_hash = hashlib.md5(str(mapping.input_path).encode()).hexdigest()[:8]
        return f"map_{timestamp}_{path_hash}"
    
    def _calculate_file_hash(self, file_path: Path) -> Optional[str]:
        """Calculate SHA-256 hash of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File hash or None if file doesn't exist
        """
        try:
            if not file_path.exists():
                return None
            
            hash_sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            self.logger.warning(f"Failed to calculate hash for {file_path}: {e}")
            return None
    
    def add_mapping(self, result: ProcessingResult) -> str:
        """Add a file mapping from processing result.
        
        Args:
            result: Processing result containing file information
            
        Returns:
            Mapping ID
        """
        # Calculate file hashes
        input_hash = self._calculate_file_hash(result.file_numbering.original_path)
        output_hash = self._calculate_file_hash(result.file_numbering.numbered_path)
        
        # Create mapping entry
        mapping = FileMappingEntry(
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
            error_message=result.error_message,
            input_hash=input_hash,
            output_hash=output_hash,
            created_at=datetime.now()
        )
        
        # Add to indexes
        self._add_mapping_to_indexes(mapping)
        
        self.logger.info(f"Added mapping: {mapping.input_path} -> {mapping.output_path}")
        return mapping.mapping_id
    
    def get_output_path(self, input_path: Path) -> Optional[Path]:
        """Get output path for a given input path.
        
        Args:
            input_path: Input file path
            
        Returns:
            Output file path or None if not found
        """
        return self.input_to_output.get(input_path)
    
    def get_input_path(self, output_path: Path) -> Optional[Path]:
        """Get input path for a given output path.
        
        Args:
            output_path: Output file path
            
        Returns:
            Input file path or None if not found
        """
        return self.output_to_input.get(output_path)
    
    def get_mapping_by_number(self, file_number: str) -> Optional[FileMappingEntry]:
        """Get mapping by file number.
        
        Args:
            file_number: File number (e.g., "01", "02")
            
        Returns:
            File mapping entry or None if not found
        """
        output_path = self.file_number_to_path.get(file_number)
        if output_path:
            return self.get_mapping_by_output_path(output_path)
        return None
    
    def get_mapping_by_input_path(self, input_path: Path) -> Optional[FileMappingEntry]:
        """Get mapping by input path.
        
        Args:
            input_path: Input file path
            
        Returns:
            File mapping entry or None if not found
        """
        output_path = self.get_output_path(input_path)
        if output_path:
            return self.get_mapping_by_output_path(output_path)
        return None
    
    def get_mapping_by_output_path(self, output_path: Path) -> Optional[FileMappingEntry]:
        """Get mapping by output path.
        
        Args:
            output_path: Output file path
            
        Returns:
            File mapping entry or None if not found
        """
        for mapping in self.mappings.values():
            if mapping.output_path == output_path:
                return mapping
        return None
    
    def get_successful_mappings(self) -> List[FileMappingEntry]:
        """Get all successful mappings.
        
        Returns:
            List of successful file mapping entries
        """
        return [m for m in self.mappings.values() if m.success]
    
    def get_failed_mappings(self) -> List[FileMappingEntry]:
        """Get all failed mappings.
        
        Returns:
            List of failed file mapping entries
        """
        return [m for m in self.mappings.values() if not m.success]
    
    def get_mappings_by_extension(self, extension: str) -> List[FileMappingEntry]:
        """Get mappings by file extension.
        
        Args:
            extension: File extension (e.g., ".md", ".txt")
            
        Returns:
            List of file mapping entries with the specified extension
        """
        return [m for m in self.mappings.values() if m.extension == extension]
    
    def get_mappings_by_folder(self, folder_path: Path) -> List[FileMappingEntry]:
        """Get mappings by folder path.
        
        Args:
            folder_path: Folder path to filter by
            
        Returns:
            List of file mapping entries in the specified folder
        """
        return [m for m in self.mappings.values() if folder_path in m.input_path.parents]
    
    def validate_mappings(self) -> List[str]:
        """Validate all mappings and return any issues found.
        
        Returns:
            List of validation error messages
        """
        issues = []
        
        for mapping in self.mappings.values():
            # Check if input file exists
            if not mapping.input_path.exists():
                issues.append(f"Input file not found: {mapping.input_path}")
            
            # Check if output file exists (for successful mappings)
            if mapping.success and not mapping.output_path.exists():
                issues.append(f"Output file not found: {mapping.output_path}")
            
            # Check for duplicate file numbers
            if mapping.file_number:
                duplicate_count = sum(1 for m in self.mappings.values() 
                                    if m.file_number == mapping.file_number)
                if duplicate_count > 1:
                    issues.append(f"Duplicate file number: {mapping.file_number}")
            
            # Check for hash mismatches
            if mapping.input_hash:
                current_hash = self._calculate_file_hash(mapping.input_path)
                if current_hash and current_hash != mapping.input_hash:
                    issues.append(f"Input file hash mismatch: {mapping.input_path}")
        
        return issues
    
    def get_mapping_statistics(self) -> Dict[str, Any]:
        """Get comprehensive mapping statistics.
        
        Returns:
            Dictionary with mapping statistics
        """
        total_mappings = len(self.mappings)
        successful_mappings = len(self.get_successful_mappings())
        failed_mappings = len(self.get_failed_mappings())
        
        # Calculate processing times
        processing_times = [m.processing_time for m in self.mappings.values()]
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
        
        # Calculate file sizes
        file_sizes = [m.file_size for m in self.mappings.values()]
        total_size = sum(file_sizes)
        avg_file_size = sum(file_sizes) / len(file_sizes) if file_sizes else 0
        
        # Calculate headline counts
        headline_counts = [m.headline_count for m in self.mappings.values()]
        total_headlines = sum(headline_counts)
        avg_headlines = sum(headline_counts) / len(headline_counts) if headline_counts else 0
        
        # Extension distribution
        extension_counts = {}
        for mapping in self.mappings.values():
            ext = mapping.extension
            extension_counts[ext] = extension_counts.get(ext, 0) + 1
        
        return {
            'total_mappings': total_mappings,
            'successful_mappings': successful_mappings,
            'failed_mappings': failed_mappings,
            'success_rate': (successful_mappings / total_mappings * 100) if total_mappings > 0 else 0,
            'avg_processing_time': avg_processing_time,
            'total_processing_time': sum(processing_times),
            'total_file_size': total_size,
            'avg_file_size': avg_file_size,
            'total_headlines': total_headlines,
            'avg_headlines': avg_headlines,
            'extension_distribution': extension_counts,
            'validation_issues': len(self.validate_mappings())
        }
    
    def export_mappings(self, format: str = 'json') -> str:
        """Export mappings in specified format.
        
        Args:
            format: Export format ('json', 'csv', 'markdown')
            
        Returns:
            Exported mappings as string
        """
        if format == 'json':
            return self._export_json()
        elif format == 'csv':
            return self._export_csv()
        elif format == 'markdown':
            return self._export_markdown()
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_json(self) -> str:
        """Export mappings as JSON."""
        data = [mapping.to_dict() for mapping in self.mappings.values()]
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _export_csv(self) -> str:
        """Export mappings as CSV."""
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Input Path', 'Output Path', 'File Number', 'Success', 
            'Processing Time', 'File Size', 'Headlines', 'Error Message'
        ])
        
        # Write data
        for mapping in self.mappings.values():
            writer.writerow([
                str(mapping.input_path),
                str(mapping.output_path),
                mapping.file_number,
                mapping.success,
                mapping.processing_time,
                mapping.file_size,
                mapping.headline_count,
                mapping.error_message or ''
            ])
        
        return output.getvalue()
    
    def _export_markdown(self) -> str:
        """Export mappings as Markdown."""
        output = ["# File Mapping Report\n"]
        
        # Statistics
        stats = self.get_mapping_statistics()
        output.append("## Statistics\n")
        output.append(f"- **Total Files**: {stats['total_mappings']}")
        output.append(f"- **Successful**: {stats['successful_mappings']}")
        output.append(f"- **Failed**: {stats['failed_mappings']}")
        output.append(f"- **Success Rate**: {stats['success_rate']:.1f}%")
        output.append(f"- **Average Processing Time**: {stats['avg_processing_time']:.2f}s")
        output.append(f"- **Total Headlines**: {stats['total_headlines']}")
        output.append("")
        
        # Successful mappings
        successful = self.get_successful_mappings()
        if successful:
            output.append("## Successfully Processed Files\n")
            for mapping in successful:
                output.append(f"- `{mapping.input_path}` → `{mapping.output_path}`")
                output.append(f"  - File Number: {mapping.file_number}")
                output.append(f"  - Headlines: {mapping.headline_count}")
                output.append(f"  - Processing Time: {mapping.processing_time:.2f}s")
                output.append("")
        
        # Failed mappings
        failed = self.get_failed_mappings()
        if failed:
            output.append("## Failed Files\n")
            for mapping in failed:
                output.append(f"- `{mapping.input_path}`")
                output.append(f"  - Error: {mapping.error_message}")
                output.append(f"  - Processing Time: {mapping.processing_time:.2f}s")
                output.append("")
        
        return "\n".join(output)
    
    def save_mappings(self) -> None:
        """Save mappings to disk."""
        try:
            mapping_file = self.mappings_dir / 'file_mappings.json'
            data = [mapping.to_dict() for mapping in self.mappings.values()]
            
            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved {len(data)} file mappings to {mapping_file}")
        except Exception as e:
            self.logger.error(f"Failed to save file mappings: {e}")
            raise FileOperationError(f"Failed to save file mappings: {e}")
    
    def clear_mappings(self) -> None:
        """Clear all mappings."""
        self.mappings.clear()
        self.input_to_output.clear()
        self.output_to_input.clear()
        self.file_number_to_path.clear()
        self.logger.info("Cleared all file mappings")
    
    def remove_mapping(self, mapping_id: str) -> bool:
        """Remove a specific mapping.
        
        Args:
            mapping_id: ID of the mapping to remove
            
        Returns:
            True if mapping was removed, False if not found
        """
        if mapping_id in self.mappings:
            mapping = self.mappings[mapping_id]
            
            # Remove from indexes
            self.input_to_output.pop(mapping.input_path, None)
            self.output_to_input.pop(mapping.output_path, None)
            if mapping.file_number:
                self.file_number_to_path.pop(mapping.file_number, None)
            
            # Remove from mappings
            del self.mappings[mapping_id]
            
            self.logger.info(f"Removed mapping: {mapping.input_path}")
            return True
        
        return False 