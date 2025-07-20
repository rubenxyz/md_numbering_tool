# Simple Input/Output Tree Example

## 📁 Input Directory
```
input/
├── docs/
│   ├── introduction.md
│   ├── getting-started.md
│   └── api-reference.md
├── images/
│   ├── logo.png
│   └── screenshot.jpg
└── config.json
```

## 📁 Output Directory (After Processing)
```
output/
├── 2025-07-20_14-30-15/                    # Timestamp-only naming
│   ├── docs/
│   │   ├── 01.1-introduction.md            # Numbered files
│   │   ├── 01.2-getting-started.md
│   │   └── 01.3-api-reference.md
│   ├── images/
│   │   ├── logo.png                        # Non-markdown files copied as-is
│   │   └── screenshot.jpg
│   ├── config.json                         # JSON files copied as-is
│   ├── batch_metadata.json                 # Processing metadata
│   ├── logs/
│   │   ├── processing.log
│   │   └── errors.log
│   └── reports/
│       └── summary_report.md
└── 2025-07-20_14-35-22/                    # Another processing run
    ├── docs/
    │   ├── introduction.md                 # Code blocks fixed (no numbering)
    │   ├── getting-started.md
    │   └── api-reference.md
    ├── images/
    │   ├── logo.png
    │   └── screenshot.jpg
    └── config.json
```

## 🔄 Processing Flow

1. **User places files** in `input/` directory
2. **Run numbering script**: `python main.py`
   - Creates `output/2025-07-20_14-30-15/`
   - Numbers markdown files: `01.1-introduction.md`
   - Copies non-markdown files as-is: `logo.png`, `config.json`
3. **Run code block fixing**: `python fix_code_blocks.py`
   - Creates `output/2025-07-20_14-35-22/`
   - Fixes HTML in markdown files
   - Copies all files (markdown + non-markdown)

## 🎯 Key Points

- **Timestamp-only naming**: `YYYY-MM-DD_HH-MM-SS` (no prefixes like "batch_" or "processed_")
- **Complete file preservation**: All files copied to output
- **Directory structure preserved**: Input hierarchy maintained
- **Processing metadata**: Logs, reports, and mappings included
- **No overwrites**: Each run creates new timestamped directory 