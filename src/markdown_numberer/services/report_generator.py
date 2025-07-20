"""Summary report generator for batch processing results."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import statistics
from dataclasses import asdict

from ..core.models import ProcessingConfig
from ..core.exceptions import FileOperationError
from .io_manager import BatchMetadata, FileMapping
from .file_mapper import FileMapper


class ReportGenerator:
    """Generates comprehensive summary reports for batch processing."""
    
    def __init__(self, output_dir: Path):
        """Initialize the report generator.
        
        Args:
            output_dir: Output directory for storing reports
        """
        self.output_dir = output_dir
        self.reports_dir = output_dir / 'reports'
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    def generate_batch_summary_report(self, 
                                    batch_metadata: BatchMetadata,
                                    file_mapper: FileMapper,
                                    config: ProcessingConfig,
                                    format: str = 'markdown') -> Path:
        """Generate a comprehensive batch summary report.
        
        Args:
            batch_metadata: Batch processing metadata
            file_mapper: File mapper with all mappings
            config: Processing configuration used
            format: Report format ('markdown', 'html', 'json')
            
        Returns:
            Path to the generated report file
        """
        try:
            # Get mapping statistics
            mapping_stats = file_mapper.get_mapping_statistics()
            
            # Generate report content
            if format == 'markdown':
                content = self._generate_markdown_report(batch_metadata, file_mapper, config, mapping_stats)
                file_extension = '.md'
            elif format == 'html':
                content = self._generate_html_report(batch_metadata, file_mapper, config, mapping_stats)
                file_extension = '.html'
            elif format == 'json':
                content = self._generate_json_report(batch_metadata, file_mapper, config, mapping_stats)
                file_extension = '.json'
            else:
                raise ValueError(f"Unsupported report format: {format}")
            
            # Save report
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = self.reports_dir / f'batch_summary_{timestamp}{file_extension}'
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Generated {format} summary report: {report_file}")
            return report_file
            
        except Exception as e:
            self.logger.error(f"Failed to generate summary report: {e}")
            raise FileOperationError(f"Failed to generate summary report: {e}")
    
    def _generate_markdown_report(self, 
                                batch_metadata: BatchMetadata,
                                file_mapper: FileMapper,
                                config: ProcessingConfig,
                                mapping_stats: Dict[str, Any]) -> str:
        """Generate markdown format report.
        
        Args:
            batch_metadata: Batch processing metadata
            file_mapper: File mapper with all mappings
            config: Processing configuration used
            mapping_stats: Mapping statistics
            
        Returns:
            Markdown report content
        """
        # Calculate additional statistics
        successful_mappings = file_mapper.get_successful_mappings()
        failed_mappings = file_mapper.get_failed_mappings()
        
        # Performance analysis
        processing_times = [m.processing_time for m in successful_mappings]
        file_sizes = [m.file_size for m in successful_mappings]
        headline_counts = [m.headline_count for m in successful_mappings]
        
        # Calculate percentiles
        time_percentiles = self._calculate_percentiles(processing_times) if processing_times else {}
        size_percentiles = self._calculate_percentiles(file_sizes) if file_sizes else {}
        headline_percentiles = self._calculate_percentiles(headline_counts) if headline_counts else {}
        
        # Extension analysis
        extension_stats = self._analyze_extensions(file_mapper)
        
        # Error analysis
        error_analysis = self._analyze_errors(failed_mappings)
        
        # Generate report
        report = f"""# Batch Processing Summary Report

## Batch Information
- **Batch ID**: {batch_metadata.batch_id}
- **Start Time**: {batch_metadata.start_time.strftime('%Y-%m-%d %H:%M:%S')}
- **End Time**: {batch_metadata.end_time.strftime('%Y-%m-%d %H:%M:%S') if batch_metadata.end_time else 'Not completed'}
- **Duration**: {batch_metadata.total_processing_time:.2f} seconds
- **Input Path**: {batch_metadata.input_path}
- **Output Path**: {batch_metadata.output_path}

## Processing Statistics
- **Total Files**: {mapping_stats['total_mappings']}
- **Successfully Processed**: {mapping_stats['successful_mappings']}
- **Failed Files**: {mapping_stats['failed_mappings']}
- **Success Rate**: {mapping_stats['success_rate']:.1f}%
- **Total Processing Time**: {mapping_stats['total_processing_time']:.2f} seconds
- **Average Processing Time**: {mapping_stats['avg_processing_time']:.2f} seconds per file

## Configuration Used
- **Start Level**: {config.start_level}
- **Max Depth**: {config.max_depth}
- **Separator**: {config.separator}
- **Preserve Existing Numbers**: {config.preserve_existing}
- **Backup Original Files**: {config.backup_original}
- **Preserve Original Names**: {config.preserve_original_name}

## Performance Analysis

### Processing Time Statistics
- **Fastest File**: {min(processing_times):.2f}s
- **Slowest File**: {max(processing_times):.2f}s
- **Median Time**: {time_percentiles.get('50', 0):.2f}s
- **95th Percentile**: {time_percentiles.get('95', 0):.2f}s

### File Size Statistics
- **Smallest File**: {min(file_sizes)} bytes
- **Largest File**: {max(file_sizes)} bytes
- **Average File Size**: {mapping_stats['avg_file_size']:.0f} bytes
- **Total Size Processed**: {mapping_stats['total_file_size']} bytes

### Headline Statistics
- **Total Headlines**: {mapping_stats['total_headlines']}
- **Average Headlines per File**: {mapping_stats['avg_headlines']:.1f}
- **Most Headlines in Single File**: {max(headline_counts) if headline_counts else 0}
- **Least Headlines in Single File**: {min(headline_counts) if headline_counts else 0}

## File Type Analysis
"""
        
        # Add extension statistics
        for ext, count in extension_stats.items():
            report += f"- **{ext}**: {count} files\n"
        
        report += "\n## Successfully Processed Files\n"
        
        # Add successful files
        for mapping in successful_mappings[:10]:  # Show first 10
            report += f"- `{mapping.input_path}` → `{mapping.output_path}`\n"
            report += f"  - File Number: {mapping.file_number}\n"
            report += f"  - Headlines: {mapping.headline_count}\n"
            report += f"  - Processing Time: {mapping.processing_time:.2f}s\n"
            report += f"  - File Size: {mapping.file_size} bytes\n"
        
        if len(successful_mappings) > 10:
            report += f"\n*... and {len(successful_mappings) - 10} more files*\n"
        
        # Add failed files if any
        if failed_mappings:
            report += "\n## Failed Files\n"
            for mapping in failed_mappings:
                report += f"- `{mapping.input_path}`\n"
                report += f"  - Error: {mapping.error_message or 'Unknown error'}\n"
                report += f"  - Processing Time: {mapping.processing_time:.2f}s\n"
        
        # Add error analysis
        if error_analysis:
            report += "\n## Error Analysis\n"
            for error_type, count in error_analysis.items():
                report += f"- **{error_type}**: {count} occurrences\n"
        
        # Add validation issues
        validation_issues = file_mapper.validate_mappings()
        if validation_issues:
            report += "\n## Validation Issues\n"
            for issue in validation_issues[:5]:  # Show first 5 issues
                report += f"- {issue}\n"
            if len(validation_issues) > 5:
                report += f"\n*... and {len(validation_issues) - 5} more issues*\n"
        
        # Add recommendations
        report += "\n## Recommendations\n"
        if mapping_stats['success_rate'] < 90:
            report += "- **Low Success Rate**: Review failed files and error patterns\n"
        if mapping_stats['avg_processing_time'] > 5.0:
            report += "- **Slow Processing**: Consider optimizing processing logic\n"
        if validation_issues:
            report += "- **Validation Issues**: Address file integrity and mapping problems\n"
        if not validation_issues and mapping_stats['success_rate'] >= 95:
            report += "- **Excellent Results**: All files processed successfully\n"
        
        report += "\n## Output Structure\n"
        report += f"- **Batch Directory**: {self.output_dir}\n"
        report += "- **File Mappings**: `mappings/file_mappings.json`\n"
        report += "- **Batch Metadata**: `batch_metadata.json`\n"
        report += "- **Processing Logs**: `logs/` directory\n"
        report += "- **Summary Reports**: `reports/` directory\n"
        
        if config.backup_original:
            report += "- **Original Backups**: `backups/` directory\n"
        
        report += "\n---\n"
        report += f"*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        return report
    
    def _generate_html_report(self, 
                            batch_metadata: BatchMetadata,
                            file_mapper: FileMapper,
                            config: ProcessingConfig,
                            mapping_stats: Dict[str, Any]) -> str:
        """Generate HTML format report.
        
        Args:
            batch_metadata: Batch processing metadata
            file_mapper: File mapper with all mappings
            config: Processing configuration used
            mapping_stats: Mapping statistics
            
        Returns:
            HTML report content
        """
        # Get data for HTML report
        successful_mappings = file_mapper.get_successful_mappings()
        failed_mappings = file_mapper.get_failed_mappings()
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Batch Processing Summary - {batch_metadata.batch_id}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: #f8f9fa; padding: 20px; border-radius: 6px; border-left: 4px solid #3498db; }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ color: #7f8c8d; font-size: 0.9em; text-transform: uppercase; }}
        .success {{ border-left-color: #27ae60; }}
        .warning {{ border-left-color: #f39c12; }}
        .error {{ border-left-color: #e74c3c; }}
        .file-list {{ background: #f8f9fa; padding: 15px; border-radius: 6px; margin: 10px 0; }}
        .file-item {{ margin: 5px 0; font-family: monospace; }}
        .config-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .config-table th, .config-table td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        .config-table th {{ background: #f8f9fa; font-weight: bold; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Batch Processing Summary Report</h1>
        
        <h2>Batch Information</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{batch_metadata.batch_id}</div>
                <div class="stat-label">Batch ID</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{batch_metadata.start_time.strftime('%Y-%m-%d %H:%M:%S')}</div>
                <div class="stat-label">Start Time</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{batch_metadata.total_processing_time:.2f}s</div>
                <div class="stat-label">Duration</div>
            </div>
        </div>
        
        <h2>Processing Statistics</h2>
        <div class="stats-grid">
            <div class="stat-card {'success' if mapping_stats['success_rate'] >= 90 else 'warning' if mapping_stats['success_rate'] >= 70 else 'error'}">
                <div class="stat-value">{mapping_stats['success_rate']:.1f}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{mapping_stats['total_mappings']}</div>
                <div class="stat-label">Total Files</div>
            </div>
            <div class="stat-card success">
                <div class="stat-value">{mapping_stats['successful_mappings']}</div>
                <div class="stat-label">Successful</div>
            </div>
            <div class="stat-card {'error' if mapping_stats['failed_mappings'] > 0 else 'success'}">
                <div class="stat-value">{mapping_stats['failed_mappings']}</div>
                <div class="stat-label">Failed</div>
            </div>
        </div>
        
        <h2>Configuration</h2>
        <table class="config-table">
            <tr><th>Setting</th><th>Value</th></tr>
            <tr><td>Start Level</td><td>{config.start_level}</td></tr>
            <tr><td>Max Depth</td><td>{config.max_depth}</td></tr>
            <tr><td>Separator</td><td>{config.separator}</td></tr>
            <tr><td>Preserve Existing</td><td>{config.preserve_existing}</td></tr>
            <tr><td>Backup Original</td><td>{config.backup_original}</td></tr>
        </table>
        
        <h2>Successfully Processed Files</h2>
        <div class="file-list">
"""
        
        # Add successful files
        for mapping in successful_mappings[:10]:
            html += f'            <div class="file-item">✓ {mapping.input_path} → {mapping.output_path}</div>\n'
        
        if len(successful_mappings) > 10:
            html += f'            <div class="file-item">... and {len(successful_mappings) - 10} more files</div>\n'
        
        html += "        </div>\n"
        
        # Add failed files if any
        if failed_mappings:
            html += "        <h2>Failed Files</h2>\n        <div class=\"file-list\">\n"
            for mapping in failed_mappings:
                html += f'            <div class="file-item">✗ {mapping.input_path} - {mapping.error_message or "Unknown error"}</div>\n'
            html += "        </div>\n"
        
        html += f"""
        <div class="footer">
            Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _generate_json_report(self, 
                            batch_metadata: BatchMetadata,
                            file_mapper: FileMapper,
                            config: ProcessingConfig,
                            mapping_stats: Dict[str, Any]) -> str:
        """Generate JSON format report.
        
        Args:
            batch_metadata: Batch processing metadata
            file_mapper: File mapper with all mappings
            config: Processing configuration used
            mapping_stats: Mapping statistics
            
        Returns:
            JSON report content
        """
        # Prepare data for JSON report
        successful_mappings = file_mapper.get_successful_mappings()
        failed_mappings = file_mapper.get_failed_mappings()
        
        report_data = {
            'report_info': {
                'generated_at': datetime.now().isoformat(),
                'format': 'json',
                'version': '1.0'
            },
            'batch_metadata': batch_metadata.to_dict(),
            'configuration': config.model_dump(),
            'statistics': mapping_stats,
            'successful_files': [mapping.to_dict() for mapping in successful_mappings],
            'failed_files': [mapping.to_dict() for mapping in failed_mappings],
            'validation_issues': file_mapper.validate_mappings(),
            'extension_analysis': self._analyze_extensions(file_mapper),
            'error_analysis': self._analyze_errors(failed_mappings)
        }
        
        return json.dumps(report_data, indent=2, ensure_ascii=False)
    
    def _calculate_percentiles(self, values: List[float]) -> Dict[str, float]:
        """Calculate percentiles for a list of values.
        
        Args:
            values: List of numeric values
            
        Returns:
            Dictionary with percentile values
        """
        if not values:
            return {}
        
        sorted_values = sorted(values)
        return {
            '25': statistics.quantiles(sorted_values, n=4)[0],
            '50': statistics.median(sorted_values),
            '75': statistics.quantiles(sorted_values, n=4)[2],
            '95': sorted_values[int(len(sorted_values) * 0.95)]
        }
    
    def _analyze_extensions(self, file_mapper: FileMapper) -> Dict[str, int]:
        """Analyze file extensions in mappings.
        
        Args:
            file_mapper: File mapper with mappings
            
        Returns:
            Dictionary with extension counts
        """
        extension_counts = {}
        for mapping in file_mapper.mappings.values():
            ext = mapping.extension
            extension_counts[ext] = extension_counts.get(ext, 0) + 1
        return extension_counts
    
    def _analyze_errors(self, failed_mappings: List[Any]) -> Dict[str, int]:
        """Analyze error patterns in failed mappings.
        
        Args:
            failed_mappings: List of failed file mappings
            
        Returns:
            Dictionary with error type counts
        """
        error_counts = {}
        for mapping in failed_mappings:
            error_msg = mapping.error_message or 'Unknown error'
            # Extract error type from message
            if 'permission' in error_msg.lower():
                error_type = 'Permission Error'
            elif 'not found' in error_msg.lower():
                error_type = 'File Not Found'
            elif 'encoding' in error_msg.lower():
                error_type = 'Encoding Error'
            elif 'syntax' in error_msg.lower():
                error_type = 'Syntax Error'
            else:
                error_type = 'Other Error'
            
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        return error_counts
    
    def generate_performance_report(self, file_mapper: FileMapper) -> str:
        """Generate a detailed performance analysis report.
        
        Args:
            file_mapper: File mapper with mappings
            
        Returns:
            Performance report content
        """
        successful_mappings = file_mapper.get_successful_mappings()
        
        if not successful_mappings:
            return "No successful mappings to analyze."
        
        # Calculate performance metrics
        processing_times = [m.processing_time for m in successful_mappings]
        file_sizes = [m.file_size for m in successful_mappings]
        headline_counts = [m.headline_count for m in successful_mappings]
        
        # Calculate correlations
        size_time_correlation = statistics.correlation(file_sizes, processing_times) if len(file_sizes) > 1 else 0
        headline_time_correlation = statistics.correlation(headline_counts, processing_times) if len(headline_counts) > 1 else 0
        
        report = f"""# Performance Analysis Report

## Processing Time Analysis
- **Mean Processing Time**: {statistics.mean(processing_times):.3f}s
- **Median Processing Time**: {statistics.median(processing_times):.3f}s
- **Standard Deviation**: {statistics.stdev(processing_times):.3f}s
- **Fastest File**: {min(processing_times):.3f}s
- **Slowest File**: {max(processing_times):.3f}s

## File Size Analysis
- **Mean File Size**: {statistics.mean(file_sizes):.0f} bytes
- **Median File Size**: {statistics.median(file_sizes):.0f} bytes
- **Total Size Processed**: {sum(file_sizes)} bytes

## Headline Analysis
- **Mean Headlines per File**: {statistics.mean(headline_counts):.1f}
- **Median Headlines per File**: {statistics.median(headline_counts):.1f}
- **Total Headlines**: {sum(headline_counts)}

## Performance Correlations
- **File Size vs Processing Time**: {size_time_correlation:.3f}
- **Headlines vs Processing Time**: {headline_time_correlation:.3f}

## Performance Recommendations
"""
        
        if size_time_correlation > 0.7:
            report += "- **High file size correlation**: Consider implementing size-based optimizations\n"
        if headline_time_correlation > 0.7:
            report += "- **High headline correlation**: Consider optimizing headline processing\n"
        if statistics.mean(processing_times) > 2.0:
            report += "- **Slow average processing**: Consider performance optimizations\n"
        if statistics.stdev(processing_times) > statistics.mean(processing_times):
            report += "- **High processing time variance**: Investigate performance bottlenecks\n"
        
        return report 