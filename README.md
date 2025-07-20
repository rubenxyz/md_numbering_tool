# Markdown Numberer

A modern Python tool for hierarchical numbering of markdown files and headlines based on parent folder numbering.

## Features

- **Hierarchical File Numbering**: Automatically numbers markdown files based on parent folder structure
- **Headline Numbering**: Adds hierarchical numbering to headlines that builds on the file's number
- **Complete Hierarchy**: Creates a consistent numbering system from folders → files → headlines
- **Code Block Fixing**: Automatically fixes HTML-encoded code blocks in markdown files
- **Modern Python**: Built with contemporary best practices, type safety, and async processing
- **High Performance**: Async file processing with controlled concurrency
- **Comprehensive Logging**: Structured logging with rich output and progress reporting

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/markdown-numberer.git
cd markdown-numberer

# Install dependencies
pip install -e .
```

### Usage

```bash
# Process markdown files with numbering
python main.py input_folder output_folder

# Example with absolute paths
python main.py /Users/ruben/Nextcloud/02\ -\ AREAS/RAG/250711\ input\ output/input /Users/ruben/Nextcloud/02\ -\ AREAS/RAG/250711\ input\ output/output
```

## Code Block Fixing

The project includes a utility script to fix HTML-encoded code blocks in markdown files. This is useful when markdown files contain code blocks with HTML `<div>`, `<p>`, and `<span>` tags instead of clean code.

### Usage

```bash
# Fix code blocks and save to new directory
python fix_code_blocks.py input_folder output_folder

# Fix code blocks in place (modify original files)
python fix_code_blocks.py input_folder
```

### Example

**Before (HTML-encoded):**
```markdown
```
<div><p><span>import</span><span> fal_client</span></p></div>
<div><p><span>handler </span><span>=</span><span> fal_client.</span><span>submit</span><span>(</span></p></div>
```
```

**After (clean Python):**
```markdown
```
import fal_client

handler = fal_client.submit(
  "fal-ai/flux/dev",
  arguments={
      "prompt": "photo of a rhino dressed suit and tie sitting at a table in a bar with a bar stools, award winning photography, Elke vogelsang"
  },
)

result = handler.get()
print(result)
```
```

### Features

- **Recursive Processing**: Automatically processes all markdown files in subdirectories
- **Smart Code Extraction**: Removes HTML tags and formats code properly
- **Pattern Recognition**: Handles common patterns like Python imports, function calls, and variable assignments
- **Safe Operation**: Can modify files in place or save to new location
- **Specific Handling**: Optimized for fal_client and other common API examples

## Example

**Input Structure:**
```
input/
├── 00.1 Introduction/
│   ├── intro.md
│   └── overview.md
└── 00.2 Getting Started/
    ├── setup.md
    └── installation.md
```

**Output Structure:**
```
output/
└── batch_2025-07-20_15-46-47/
    ├── logs/
    │   ├── batch.log
    │   ├── processing.log
    │   ├── errors.log
    │   └── performance.log
    ├── mappings/
    │   └── file_mappings.json
    ├── reports/
    │   ├── batch_summary.md
    │   ├── batch_summary.html
    │   └── batch_summary.json
    ├── backups/
    └── 00.1 Introduction/
        ├── 00.1.1-intro.md
        └── 00.1.2-overview.md
    └── 00.2 Getting Started/
        ├── 00.2.1-setup.md
        └── 00.2.2-installation.md
```

**Numbered Content Example:**
```markdown
# 00.1.1.1 Introduction
## 00.1.1.1.1 What is this guide
## 00.1.1.1.2 Who should read this

# 00.1.2.1 Overview  
## 00.1.2.1.1 System architecture
### 00.1.2.1.1.1 Core components
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/markdown-numberer.git
cd markdown-numberer

# Install dependencies
pip install -e .

# Activate virtual environment (if using one)
source venv/bin/activate  # or your preferred method
```

### Testing the Script

```bash
# Test with sample files
python main.py input output

# Test with your own files
python main.py /path/to/your/input /path/to/your/output

# Test code block fixing
python fix_code_blocks.py input output_fixed
```

## Configuration

The script uses sensible defaults for most settings. If you need to customize the behavior, you can modify the `create_default_config()` function in `main.py`:

```python
def create_default_config(input_path: Path, output_path: Path) -> ProcessingConfig:
    return ProcessingConfig(
        input_path=input_path,
        output_path=output_path,
        start_level=1,                    # Starting level for numbering
        max_depth=6,                      # Maximum depth for headlines
        separator=".",                    # Separator for hierarchical numbers
        preserve_existing=False,          # Whether to preserve existing numbering
        sorting_method="alphabetical",    # File sorting method
        filename_separator="-",           # Separator between number and filename
        preserve_original_name=True,      # Keep original filename
        include_patterns=["*.md", "*.markdown"],  # File patterns to process
        exclude_patterns=["**/.*", "**/*temp*"],  # File patterns to exclude
        max_concurrent_files=10,          # Concurrent processing limit
        log_level="INFO",                 # Logging level
        # ... other settings
    )
```

## Architecture

The project follows modern Python architecture patterns:

- **Type Safety**: Full type hints with Pydantic validation
- **Async Processing**: High-performance async file handling
- **Service Architecture**: Clean separation of concerns
- **Configuration Management**: Pydantic-based validation
- **Error Handling**: Comprehensive exception hierarchy
- **Logging**: Structured logging with multiple output formats

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the script with your changes
5. Ensure the script works correctly
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Roadmap

- [ ] Configuration file support (YAML/JSON)
- [ ] Command-line argument customization
- [ ] Batch processing with custom batch IDs
- [ ] Performance optimization for large file sets
- [ ] Additional output formats (PDF, HTML)
- [ ] Plugin architecture for custom numbering strategies
- [ ] Enhanced code block fixing with language detection 