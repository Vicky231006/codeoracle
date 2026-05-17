# CodeOracle Ingestion Pipeline

The ingestion pipeline processes code repositories (Python or JavaScript/TypeScript) and extracts structural information into a standardized JSON manifest format.

## Installation

```bash
cd ingest
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
python ingest.py --source <path|url|zip> --output <output_path> [--language python|javascript]
```

### Parameters

- `--source`: (Required) Source of the repository:
  - Local file path: `/path/to/repo`
  - GitHub URL: `https://github.com/user/repo`
  - ZIP file: `/path/to/repo.zip`
  
- `--output`: (Required) Output path for the JSON manifest file

- `--language`: (Optional) Primary language of the repository. Auto-detected if not specified.
  - Choices: `python`, `javascript`, `typescript`

### Examples

**Local repository:**
```bash
python ingest.py --source /path/to/repo --output ../demo/repo_manifest.json
```

**GitHub URL:**
```bash
python ingest.py --source https://github.com/pallets/flask --output ../demo/flask_manifest.json
```

**ZIP file:**
```bash
python ingest.py --source repo.zip --output ../demo/repo_manifest.json
```

## Output Schema

The pipeline generates a JSON file with the following structure:

```json
{
  "repo_name": "string",
  "language_primary": "string",
  "total_files": "integer",
  "total_lines": "integer",
  "ingested_at": "ISO 8601 timestamp",
  "files": [
    {
      "path": "string (relative)",
      "language": "string",
      "lines": "integer",
      "size_bytes": "integer",
      "imports": ["string"],
      "exports": ["string"],
      "functions": ["string"],
      "classes": ["string"],
      "complexity_score": "float (0-100)",
      "last_modified": "ISO 8601 or null",
      "is_test_file": "boolean",
      "is_config_file": "boolean",
      "raw_content": "string (truncated to 8000 chars)"
    }
  ],
  "dependency_graph": {
    "nodes": [{"id": "filepath", "label": "filename"}],
    "edges": [{"source": "filepath", "target": "filepath", "type": "import|require"}]
  },
  "entry_points": ["string"],
  "external_dependencies": [{"name": "string", "version": "string or unknown"}]
}
```

## Features

### File Parsing

**Python Files (.py):**
- Extracts imports, functions, classes using AST
- Calculates cyclomatic complexity
- Identifies module-level exports

**JavaScript/TypeScript Files (.js, .jsx, .ts, .tsx):**
- Extracts imports (ES6, CommonJS, dynamic)
- Identifies functions (declarations, arrow functions, methods)
- Extracts classes and exports
- Calculates complexity metrics

### Automatic Detection

**Test Files:**
- `test_*.py`, `*_test.py`
- `*.test.js`, `*.spec.js`
- Files in `/tests/`, `/test/`, `/__tests__/` directories

**Config Files:**
- `config.*`, `setup.py`, `package.json`
- `requirements.txt`, `.env*`
- `*.config.js`, `tsconfig.json`, etc.

**Entry Points:**
- `main.py`, `__main__.py`, `app.py`, `server.py`
- `index.js`, `app.js`, `server.js`, `main.js`
- Python files with `if __name__ == "__main__"`

### Dependency Graph

The pipeline builds a graph showing file dependencies:
- **Nodes**: Each file in the repository
- **Edges**: Import relationships between files
- Only includes internal dependencies (not external packages)

### External Dependencies

Extracts package dependencies from:
- **Python**: `requirements.txt`, `Pipfile`, `setup.py`
- **JavaScript**: `package.json` (dependencies and devDependencies)

### Complexity Scoring

Calculates cyclomatic complexity by counting decision points:
- Conditional statements (if, elif, else)
- Loops (for, while, do-while)
- Exception handlers (try/catch)
- Logical operators (and, or, &&, ||)
- Ternary operators
- Switch cases

Score is normalized to 0-100 scale.

## File Filtering

**Processed Extensions:**
- Python: `.py`
- JavaScript/TypeScript: `.js`, `.jsx`, `.ts`, `.tsx`

**Skipped Directories:**
- `node_modules/`, `venv/`, `__pycache__/`
- `.git/`, `dist/`, `build/`
- `.venv/`, `env/`, `.env/`
- `coverage/`, `.pytest_cache/`, `.mypy_cache/`

## Performance

- Processes ~200 files in under 30 seconds
- Progress logged every 10 files
- Graceful error handling (skips unparseable files)
- Content truncated to 8000 characters per file

## Architecture

```
ingest/
├── ingest.py              # Main ingestion script
├── parsers/
│   ├── __init__.py        # Package initialization
│   ├── python_parser.py   # Python AST parser
│   └── js_parser.py       # JavaScript/TypeScript parser
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Error Handling

The pipeline handles errors gracefully:
- Parse errors: Logs warning, continues with next file
- Missing files: Returns error message
- Invalid repositories: Exits with error code 1
- Temporary files: Automatically cleaned up

## Logging

Uses Python's logging module with INFO level:
- Repository processing start/completion
- File count progress (every 10 files)
- Dependency graph building
- Entry point detection
- External dependency extraction
- Final statistics

## Testing

A test repository is included in `../demo/test_repo/` with:
- Main entry point (`main.py`)
- Utility module (`utils.py`)
- Configuration file (`config.py`)
- Test file (`tests/test_main.py`)
- External dependencies (`requirements.txt`)

Run the test:
```bash
python ingest.py --source ../demo/test_repo --output ../demo/test_manifest.json
```

Expected output:
- 4 files processed
- 2 entry points detected (main.py, test_main.py)
- Dependency edges between files
- 4 external dependencies extracted
- config.py marked as config file
- test_main.py marked as test file

## Future Enhancements

Potential improvements for future versions:
- Support for more languages (Java, Go, Rust, etc.)
- More sophisticated dependency resolution
- Git history analysis (commit frequency, authors)
- Code quality metrics (duplication, maintainability)
- Documentation coverage analysis
- Security vulnerability scanning