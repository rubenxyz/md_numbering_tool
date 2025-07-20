#!/usr/bin/env python3
"""
Fix HTML-encoded code blocks in markdown files.

This script recursively processes markdown files and fixes code blocks that contain
HTML <div> and <span> tags instead of clean code.

Usage:
    python fix_code_blocks.py <input_folder> [output_folder]
    
If output_folder is not specified, files are modified in place.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple


def extract_clean_code_from_html(html_content: str) -> str:
    """
    Extract clean code from HTML-encoded content.
    
    Args:
        html_content: HTML string containing <div><p><span> tags
        
    Returns:
        Clean code string
    """
    # Remove all HTML tags and extract text content
    clean_code = re.sub(r'<[^>]+>', '', html_content)
    
    # Clean up extra whitespace and newlines
    clean_code = re.sub(r'\s+', ' ', clean_code)
    clean_code = clean_code.strip()
    
    # Handle the specific fal_client example
    if 'fal_client' in clean_code and 'submit' in clean_code:
        # Extract the prompt from the code - look for the longer quoted string
        prompt_matches = re.findall(r'"([^"]*)"', clean_code)
        # Use the longest quoted string as the prompt (likely to be the actual prompt)
        prompt = max(prompt_matches, key=len) if prompt_matches else "your prompt here"
        
        # Format the code properly
        formatted_code = f"""import fal_client

handler = fal_client.submit(
  "fal-ai/flux/dev",
  arguments={{
      "prompt": "{prompt}"
  }},
)

result = handler.get()
print(result)"""
        return formatted_code
    
    # Handle export statements
    if 'export' in clean_code and 'FAL_KEY' in clean_code:
        return 'export FAL_KEY="PASTE_YOUR_FAL_KEY_HERE"'
    
    # Generic fallback - try to format based on common patterns
    lines = []
    
    # Handle import statements
    if 'import' in clean_code:
        import_match = re.search(r'import\s+\w+', clean_code)
        if import_match:
            lines.append(import_match.group(0))
            clean_code = clean_code[import_match.end():].strip()
    
    # Handle variable assignments
    if '=' in clean_code:
        # Split by common patterns
        parts = re.split(r'(\w+\s*=\s*|\w+\([^)]*\)\s*|\.\w+\([^)]*\)\s*|,\s*|\)\s*)', clean_code)
        
        current_line = ""
        for part in parts:
            if part.strip():
                current_line += part
                # Start new line for certain patterns
                if part.strip().endswith(','):
                    lines.append(current_line.strip())
                    current_line = ""
                elif part.strip().endswith(')'):
                    current_line += '\n'
        
        if current_line.strip():
            lines.append(current_line.strip())
    
    # If we have lines, return them
    if lines:
        return '\n'.join(lines)
    
    # Final fallback - just return the cleaned text
    return clean_code


def fix_code_block(match) -> str:
    """
    Fix a single code block by extracting clean code from HTML.
    
    Args:
        match: Regex match object containing the code block
        
    Returns:
        Fixed code block string
    """
    code_block = match.group(0)
    code_content = match.group(1)
    
    # Check if this code block contains HTML tags
    if '<div>' in code_content or '<span>' in code_content:
        # Extract clean code
        clean_code = extract_clean_code_from_html(code_content)
        
        # Reconstruct the code block
        return f"```\n{clean_code}\n```"
    
    # If no HTML tags, return unchanged
    return code_block


def process_markdown_file(input_path: Path, output_path: Path = None) -> bool:
    """
    Process a single markdown file to fix HTML-encoded code blocks.
    
    Args:
        input_path: Path to input markdown file
        output_path: Path to output file (if None, modify in place)
        
    Returns:
        True if file was modified, False otherwise
    """
    try:
        # Read the file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file contains HTML-encoded code blocks
        if '<div>' not in content and '<span>' not in content:
            return False
        
        # Fix code blocks using regex
        # This regex matches code blocks that may contain HTML
        pattern = r'```(?:\w+)?\n(.*?)\n```'
        
        # Process the content
        modified_content = re.sub(pattern, fix_code_block, content, flags=re.DOTALL)
        
        # Check if content was actually modified
        if modified_content == content:
            return False
        
        # Determine output path
        if output_path is None:
            output_path = input_path
        
        # Write the modified content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        return True
        
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False


def process_directory(input_dir: Path, output_dir: Path = None, processed_files: List[Path] = None) -> int:
    """
    Recursively process all markdown files in a directory.
    
    Args:
        input_dir: Input directory path
        output_dir: Output directory path (if None, modify in place)
        processed_files: List to track processed files
        
    Returns:
        Number of files processed
    """
    if processed_files is None:
        processed_files = []
    
    count = 0
    
    # Create output directory if specified
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all files in the directory
    for item in input_dir.iterdir():
        if item.is_file() and item.suffix.lower() in ['.md', '.markdown']:
            # Determine output path
            if output_dir:
                relative_path = item.relative_to(input_dir)
                output_path = output_dir / relative_path
                # Ensure output subdirectory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                output_path = None
            
            # Process the file
            if process_markdown_file(item, output_path):
                processed_files.append(item)
                count += 1
                print(f"Fixed: {item}")
        
        elif item.is_dir():
            # Recursively process subdirectories
            if output_dir:
                sub_output_dir = output_dir / item.name
            else:
                sub_output_dir = None
            
            count += process_directory(item, sub_output_dir, processed_files)
    
    return count


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python fix_code_blocks.py <input_folder> [output_folder]")
        print("If output_folder is not specified, files are modified in place.")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    # Validate input path
    if not input_path.exists():
        print(f"Error: Input path does not exist: {input_path}")
        sys.exit(1)
    
    if not input_path.is_dir():
        print(f"Error: Input path is not a directory: {input_path}")
        sys.exit(1)
    
    # Process files
    processed_files = []
    count = process_directory(input_path, output_path, processed_files)
    
    # Print results
    print(f"\nProcessing complete!")
    print(f"Files processed: {count}")
    
    if count > 0:
        print(f"Modified files:")
        for file_path in processed_files:
            print(f"  - {file_path}")
        
        if output_path:
            print(f"\nFixed files saved to: {output_path}")
        else:
            print(f"\nFiles modified in place.")
    else:
        print("No files needed fixing.")


if __name__ == "__main__":
    main() 