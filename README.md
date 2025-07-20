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
- **Hardcoded Directories**: Uses fixed input/output folders for consistent workflow

## Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation
```bash
# Clone and setup
git clone <repository>
cd md-numbering
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Usage

### Quick Start

1. **Place your files** in the `input/` directory
2. **Run the numbering script**:
   ```bash
   python main.py
   ```
3. **Run the code block fixing script**:
   ```bash
   python fix_code_blocks.py
   ```
4. **Check results** in the `output/` directory

### Output Structure

Both scripts create timestamped subfolders in the `output/` directory:

```
output/
├── 2025-07-20_18-44-10/          # Markdown numbering results
│   ├── 250720 fal/
│   │   ├── 01. fal/
│   │   │   ├── 01.1 Introduction  fal.ai Docs  fal.ai Docs.md
│   │   │   ├── 01.2 Quickstart with fal  fal.ai Docs  fal.ai Docs.md
│   │   │   └── ...
│   │   └── 02. Models/
│   │       ├── 02.1-seedream3.md
│   │       ├── 02.1-flux1_kontext_max_multi-img.md
│   │       └── ...
│   ├── batch_metadata.json
│   ├── logs/
│   ├── mappings/
│   └── reports/
└── 2025-07-20_18-40-02/          # Code block fixing results
    └── 250720 fal/
        ├── 01. fal/
        │   ├── 01.1 Introduction  fal.ai Docs  fal.ai Docs.md
        │   ├── 01.2 Quickstart with fal  fal.ai Docs  fal.ai Docs.md
        │   └── ...
        └── 02. Models/
            ├── seedream3.md
            ├── seedream3.json
            ├── flux1_kontext_max_multi-img.md
            ├── flux1_kontext_max_multi-img.json
            └── ...
```

## Directory Structure

**Important**: Both scripts use hardcoded input and output directories and create timestamped subfolders:

- **Input Directory**: `input/` - Place your markdown files here
- **Output Directory**: `output/` - Processed files are saved in timestamped subfolders

### Required Folder Structure
```
project/
├── input/           # ← Hardcoded input folder
│   ├── 01. Introduction/
│   │   ├── intro.md
│   │   └── setup.md
│   └── 02. Tutorial/
│       └── getting-started.md
├── output/          # ← Hardcoded output folder
│   ├── batch_2025-01-20_14-30-25/     # ← Timestamped numbering results
│   │   ├── logs/
│   │   ├── reports/
│   │   ├── 01.1-intro.md
│   │   └── 02.1-getting-started.md
│   └── code_blocks_fixed_2025-01-20_14-35-12/  # ← Timestamped code block fixes
│       ├── 01. Introduction/
│       └── 02. Tutorial/
├── main.py
├── fix_code_blocks.py
└── README.md
```

### Timestamped Output Structure

Both scripts create timestamped subfolders in the `output/` directory:

**Main Numbering Script:**
- **Folder Name**: `batch_YYYY-MM-DD_HH-MM-SS/`
- **Contents**: Numbered markdown files, logs, reports, mappings

**Code Block Fixing Script:**
- **Folder Name**: `code_blocks_fixed_YYYY-MM-DD_HH-MM-SS/`
- **Contents**: Fixed markdown files with clean code blocks

## Features

### Markdown Numbering

Automatically numbers headlines in markdown files with hierarchical numbering.

**Before:**
```markdown
# Introduction
## Overview
### Getting Started
## Installation
```

**After:**
```markdown
# 01.1 Introduction
## 01.1.1 Overview
### 01.1.1.1 Getting Started
## 01.1.2 Installation
```

#### Markdown Numbering Features
- **Hierarchical Numbering**: Maintains proper headline hierarchy (01.1, 01.1.1, etc.)
- **Recursive Processing**: Automatically processes all subdirectories
- **File Renaming**: Adds numbered prefixes to filenames (e.g., `01.1-introduction.md`)
- **Smart Sorting**: Maintains alphabetical order within each level
- **Hardcoded Directories**: Uses `input/` and `output/` folders automatically
- **Timestamped Output**: Creates output subfolders with format `YYYY-MM-DD_HH-MM-SS`
- **Comprehensive Verification**: Validates all files were processed correctly

### Verification Systems

Both scripts include comprehensive verification to ensure processing quality:

#### Markdown Numbering Script Verification
- **File Count Validation**: Ensures all input files have corresponding output files
- **Success Rate Calculation**: Reports percentage of successful processing
- **File Mapping Validation**: Checks file integrity and numbering consistency
- **Processing Statistics**: Detailed metrics on processing time, file sizes, headlines
- **Error Reporting**: Comprehensive error logging and reporting

**Example Output:**
```
Total files: 38
Processed: 38
Failed: 0
Success rate: 100.0%
Total headlines processed: 301
```

#### Code Block Fixing Script Verification
- **HTML Removal Verification**: Confirms HTML tags were successfully removed
- **Code Block Counting**: Tracks how many code blocks were fixed
- **Content Preservation**: Ensures no content was lost during processing
- **Batch Verification**: Validates entire processing operation
- **Success Rate Reporting**: Shows verification success percentage

**Example Output:**
```
📊 Verification Results:
  • Input files: 54
  • Output files: 54
  • Files verified: 54
  • Verification passed: 54
  • Verification failed: 0
  • Success rate: 100.0%
  • HTML code blocks removed: 90
  • Total code blocks fixed: 90

✅ Verification PASSED - High success rate!
```

#### Verification Benefits
- **Quality Assurance**: Ensures processing meets expected standards
- **Error Detection**: Identifies and reports processing issues
- **Transparency**: Provides detailed metrics on processing results
- **Confidence**: Gives users assurance that files were processed correctly
- **Debugging**: Helps identify and resolve processing problems

## Configuration

### Hardcoded Directory Requirements

Both scripts are designed to work with fixed input and output directories:

1. **Input Directory**: Must be named `input/` in the project root
2. **Output Directory**: Must be named `output/` in the project root
3. **Timestamped Subfolders**: Results are saved in timestamped subfolders within `output/`
4. **No Command Line Arguments**: Scripts run automatically without parameters
5. **Consistent Workflow**: Same directory structure for all operations

### Why Hardcoded Directories?
- **Simplified Usage**: No need to remember or specify paths
- **Consistent Workflow**: Same behavior across different projects
- **Error Prevention**: Eliminates path-related mistakes
- **Automation Friendly**: Easy to integrate into automated workflows
- **Version Control**: Timestamped outputs preserve processing history

## Development

### Project Structure
```
src/markdown_numberer/
├── core/           # Core numbering logic
├── services/       # File processing services
└── __init__.py
```

### Testing
```bash
# Run the markdown numbering script
python main.py

# Run the code block fixing script
python fix_code_blocks.py

# Check results in output/ directory
ls output/
```

### Adding New Features
1. Follow the existing hardcoded directory pattern
2. Use `input/` for source files
3. Use `output/` for processed results
4. Maintain the same simple command-line interface
5. Use timestamp-only format for output subfolders

## License

[Add your license information here]