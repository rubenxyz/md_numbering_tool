# Markdown Numberer

A modern Python tool for hierarchical numbering of markdown files and headlines based on parent folder numbering.

## Features

- **Hierarchical File Numbering**: Automatically numbers markdown files based on parent folder structure
- **Headline Numbering**: Adds hierarchical numbering to headlines that builds on the file's number
- **Complete Hierarchy**: Creates a consistent numbering system from folders → files → headlines
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

# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/markdown_numberer

# Run specific test categories
pytest -m unit
pytest -m integration
pytest -m async
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

## Configuration

The tool supports configuration via YAML files:

```yaml
numbering:
  start_level: 1
  max_depth: 6
  separator: "."
  preserve_existing: false

files:
  sorting_method: "alphabetical"  # alphabetical, creation_date, modification_date, size, custom
  filename_separator: "-"
  preserve_original_name: true
  include_patterns: ["*.md", "*.markdown"]
  exclude_patterns: ["**/.*", "**/*temp*"]

logging:
  level: "INFO"
  format: "structured"
```

## Architecture

The project follows modern Python architecture patterns:

- **Type Safety**: Full type hints with mypy validation
- **Async Processing**: High-performance async file handling
- **Dependency Injection**: Clean service architecture
- **Configuration Management**: Pydantic-based validation
- **Error Handling**: Comprehensive exception hierarchy
- **Testing**: Modern pytest patterns with property-based testing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass and code quality checks succeed
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Roadmap

- [ ] Plugin architecture for custom numbering strategies
- [ ] Web UI for interactive processing
- [ ] API server for remote processing
- [ ] Real-time processing with WebSocket updates
- [ ] Database integration for processing history
- [ ] Container support with Docker images 