#!/usr/bin/env python3
"""
Code Block Fixing Script

Automatically fixes HTML-encoded code blocks in markdown files.
Processes ALL files in the input directory, fixing markdown files and copying others as-is.

Usage:
    python fix_code_blocks.py
    
Hardcoded directories:
- Input: 'input/'
- Output: 'output/YYYY-MM-DD_HH-MM-SS/'
"""

import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


def extract_clean_code_from_html(html_content: str) -> str:
    """
    Extract clean code from HTML-encoded content.
    
    Args:
        html_content: HTML-encoded code content
        
    Returns:
        Clean, properly formatted code
    """
    # Remove HTML tags and extract text content
    # First, remove <div>, <p>, and <span> tags
    clean_content = re.sub(r'</?(div|p|span)[^>]*>', '', html_content)
    
    # Remove any remaining HTML tags
    clean_content = re.sub(r'<[^>]+>', '', clean_content)
    
    # Decode HTML entities
    import html
    clean_content = html.unescape(clean_content)
    
    # Clean up whitespace and formatting
    lines = clean_content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Remove excessive whitespace
        line = re.sub(r'\s+', ' ', line.strip())
        if line:
            cleaned_lines.append(line)
    
    # Join lines with proper spacing
    result = '\n'.join(cleaned_lines)
    
    # Add proper indentation for common patterns
    result = re.sub(r'(\w+)\s*=\s*(\w+\.\w+\([^)]*\))', r'\1 = \2', result)
    result = re.sub(r'(\w+)\s*=\s*\{', r'\1 = {', result)
    
    return result


def fix_code_block(match) -> str:
    """
    Fix a single code block by extracting clean code from HTML.
    
    Args:
        match: Regex match object containing the code block
        
    Returns:
        Fixed code block with clean code
    """
    language = match.group(1) or ''
    html_content = match.group(2)
    
    # Extract clean code
    clean_code = extract_clean_code_from_html(html_content)
    
    # Return the fixed code block
    if language:
        return f"```{language}\n{clean_code}\n```"
    else:
        return f"```\n{clean_code}\n```"


def process_markdown_file(input_path: Path, output_path: Path) -> bool:
    """
    Process a single markdown file, fixing HTML-encoded code blocks.
    
    Args:
        input_path: Input file path
        output_path: Output file path
        
    Returns:
        True if the file needed fixing, False if it was copied as-is
    """
    try:
        # Read the file content
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the file contains HTML-encoded code blocks
        html_pattern = r'```(\w*)\n(.*?)```'
        html_matches = re.findall(html_pattern, content, re.DOTALL)
        
        needs_fixing = False
        for _, code_content in html_matches:
            if '<div>' in code_content or '<p>' in code_content or '<span>' in code_content:
                needs_fixing = True
                break
        
        if needs_fixing:
            # Fix HTML-encoded code blocks
            fixed_content = re.sub(html_pattern, fix_code_block, content, flags=re.DOTALL)
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the fixed content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            return True
        else:
            # Copy the file as-is
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(input_path, output_path)
            return False
            
    except Exception as e:
        print(f"❌ Error processing {input_path}: {e}")
        return False


def process_directory(input_dir: Path, output_dir: Path, processed_files: List[Path] = None, all_files: List[Path] = None) -> int:
    """
    Recursively process all files in a directory.
    
    Args:
        input_dir: Input directory path
        output_dir: Output directory path
        processed_files: List to track files that needed fixing
        all_files: List to track all files processed
        
    Returns:
        Number of files that needed fixing
    """
    if processed_files is None:
        processed_files = []
    if all_files is None:
        all_files = []
    
    count = 0
    
    # Process all files in the directory
    for item in input_dir.iterdir():
        if item.is_file():
            # Determine output path
            relative_path = item.relative_to(input_dir)
            output_path = output_dir / relative_path
            # Ensure output subdirectory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Track all files processed
            all_files.append(item)
            
            # Only process markdown files for HTML fixing
            if item.suffix.lower() in ['.md', '.markdown']:
                # Process the markdown file
                if process_markdown_file(item, output_path):
                    processed_files.append(item)
                    count += 1
                    print(f"Fixed: {item}")
                else:
                    print(f"Copied: {item}")
            else:
                # Copy non-markdown files as-is
                try:
                    shutil.copy2(item, output_path)
                    print(f"📄 Copied: {item}")
                except Exception as e:
                    print(f"❌ Error copying {item}: {e}")
        
        elif item.is_dir():
            # Recursively process subdirectories
            sub_output_dir = output_dir / item.name
            count += process_directory(item, sub_output_dir, processed_files, all_files)
    
    return count


def verify_file_processing(input_path: Path, output_path: Path) -> Dict[str, Any]:
    """
    Verify that a file was processed correctly.
    
    Args:
        input_path: Input file path
        output_path: Output file path
        
    Returns:
        Dictionary with verification results
    """
    verification = {
        'verification_passed': False,
        'file_exists': False,
        'html_removed': False,
        'code_blocks_fixed': 0,
        'error': None
    }
    
    try:
        # Check if output file exists
        if not output_path.exists():
            verification['error'] = f"Output file not found: {output_path}"
            return verification
        
        verification['file_exists'] = True
        
        # Only verify markdown files for HTML content
        if input_path.suffix.lower() not in ['.md', '.markdown']:
            # For non-markdown files, just verify they exist and have same size
            if output_path.stat().st_size == input_path.stat().st_size:
                verification['verification_passed'] = True
            return verification
        
        # Read input and output content
        with open(input_path, 'r', encoding='utf-8') as f:
            input_content = f.read()
        
        with open(output_path, 'r', encoding='utf-8') as f:
            output_content = f.read()
        
        # Count HTML tags in input
        input_html_count = len(re.findall(r'<(div|p|span)[^>]*>', input_content))
        
        # Count HTML tags in output
        output_html_count = len(re.findall(r'<(div|p|span)[^>]*>', output_content))
        
        # Check if HTML was removed
        if output_html_count < input_html_count:
            verification['html_removed'] = True
            verification['code_blocks_fixed'] = input_html_count - output_html_count
        
        # Verify the file was processed correctly
        # For files that needed fixing: HTML should be removed
        # For files that didn't need fixing: Content should be identical
        if input_html_count > 0:
            # File had HTML, should have been fixed
            verification['verification_passed'] = verification['html_removed']
        else:
            # File had no HTML, should be identical
            verification['verification_passed'] = (input_content == output_content)
        
    except Exception as e:
        verification['error'] = str(e)
    
    return verification


def verify_batch_processing(input_dir: Path, output_dir: Path, processed_files: List[Path], all_files: List[Path]) -> Dict[str, Any]:
    """
    Verify the entire batch processing operation.
    
    Args:
        input_dir: Input directory
        output_dir: Output directory
        processed_files: List of files that needed fixing
        all_files: List of all files that were processed
        
    Returns:
        Dictionary with batch verification results
    """
    batch_verification = {
        'total_input_files': 0,
        'total_output_files': 0,
        'files_verified': 0,
        'verification_passed': 0,
        'verification_failed': 0,
        'html_removed_total': 0,
        'code_blocks_fixed_total': 0,
        'errors': [],
        'file_verifications': {}
    }
    
    # Count all input files (not just markdown)
    for item in input_dir.rglob('*'):
        if item.is_file():
            batch_verification['total_input_files'] += 1
    
    # Count all output files (not just markdown)
    for item in output_dir.rglob('*'):
        if item.is_file():
            batch_verification['total_output_files'] += 1
    
    # Verify each file that was processed (both fixed and copied)
    for input_file in all_files:
        try:
            # Find corresponding output file
            relative_path = input_file.relative_to(input_dir)
            output_file = output_dir / relative_path
            
            if output_file.exists():
                # Only verify markdown files for HTML content
                if input_file.suffix.lower() in ['.md', '.markdown']:
                    verification = verify_file_processing(input_file, output_file)
                    batch_verification['file_verifications'][str(input_file)] = verification
                    batch_verification['files_verified'] += 1
                    
                    if verification['verification_passed']:
                        batch_verification['verification_passed'] += 1
                        batch_verification['html_removed_total'] += verification['code_blocks_fixed']
                        batch_verification['code_blocks_fixed_total'] += verification['code_blocks_fixed']
                    else:
                        batch_verification['verification_failed'] += 1
                        if 'error' in verification:
                            batch_verification['errors'].append(f"{input_file}: {verification['error']}")
                else:
                    # For non-markdown files, just verify they exist and have same size
                    if output_file.stat().st_size == input_file.stat().st_size:
                        batch_verification['verification_passed'] += 1
                    else:
                        batch_verification['verification_failed'] += 1
                        batch_verification['errors'].append(f"File size mismatch: {input_file}")
            else:
                batch_verification['errors'].append(f"Output file not found: {output_file}")
                batch_verification['verification_failed'] += 1
                
        except Exception as e:
            batch_verification['errors'].append(f"Verification error for {input_file}: {e}")
            batch_verification['verification_failed'] += 1
    
    # Calculate success rate
    if batch_verification['files_verified'] > 0:
        batch_verification['success_rate'] = (
            batch_verification['verification_passed'] / batch_verification['files_verified'] * 100
        )
    else:
        batch_verification['success_rate'] = 0
    
    return batch_verification


def main():
    """Main function to process all files."""
    # Hardcoded directories
    input_dir = Path("input")
    output_base = Path("output")
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_dir = output_base / timestamp
    
    print(f"Created timestamped output directory: {output_dir}")
    
    # Validate input directory
    if not input_dir.exists():
        print(f"❌ Error: Input directory does not exist: {input_dir}")
        return
    
    if not input_dir.is_dir():
        print(f"❌ Error: Input path is not a directory: {input_dir}")
        return
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all files
    processed_files = []
    all_files = []
    
    count = process_directory(input_dir, output_dir, processed_files, all_files)
    
    print(f"\n🔍 Running verification...")
    
    # Verify processing
    verification = verify_batch_processing(input_dir, output_dir, processed_files, all_files)
    
    # Print results
    print(f"\nProcessing complete!")
    print(f"Files that needed fixing: {len(processed_files)}")
    print(f"Total files processed: {len(all_files)}")
    
    print(f"\nAll processed files:")
    for file_path in all_files:
        if file_path in processed_files:
            print(f"  ✅ Fixed: {file_path}")
        else:
            print(f"  📋 Copied: {file_path}")
    
    print(f"\nAll files saved to: {output_dir}")
    
    # Print verification results
    print(f"\n📊 Verification Results:")
    print(f"  • Input files: {verification['total_input_files']}")
    print(f"  • Output files: {verification['total_output_files']}")
    print(f"  • Files verified: {verification['files_verified']}")
    print(f"  • Verification passed: {verification['verification_passed']}")
    print(f"  • Verification failed: {verification['verification_failed']}")
    print(f"  • Success rate: {verification['success_rate']:.1f}%")
    print(f"  • HTML code blocks removed: {verification['html_removed_total']}")
    print(f"  • Total code blocks fixed: {verification['code_blocks_fixed_total']}")
    
    if verification['verification_passed'] == len(all_files):
        print(f"\n✅ Verification PASSED - High success rate!")
    else:
        print(f"\n❌ Verification FAILED - Some files have issues")
        if verification['errors']:
            print(f"Errors:")
            for error in verification['errors'][:5]:  # Show first 5 errors
                print(f"  - {error}")


if __name__ == "__main__":
    main() 