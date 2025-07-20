# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Testing and Quality Assurance
- Run tests: `uv run pytest`
- Type checking: `uv run mypy --strict tga_shortage_scraper tests/`  
- Linting: `uv run ruff check tga_shortage_scraper tests`
- Formatting: `uv run ruff fmt tga_shortage_scraper tests`
- Run single test: `uv run pytest tests/test_click.py::test_command_help`

### Running the Application
- Run scraper: `uv run python -m tga_shortage_scraper`
- Run with ingredient filter: `uv run python -m tga_shortage_scraper --ingredient "paracetamol"`
- Show help: `uv run python -m tga_shortage_scraper --help`

### Package Management
- Install dependencies: `uv sync`
- Add new dependency: `uv add <package>`
- Add dev dependency: `uv add --dev <package>`

## Project Architecture

### Core Purpose
This is a CLI tool that scrapes the Australian TGA (Therapeutic Goods Administration) shortage database for ARTG (Australian Register of Therapeutic Goods) entries. It fetches CSV data from the TGA API and converts it to structured JSON output.

### Main Components

#### Data Models (`tga_shortage_scraper/__init__.py`)
- `ArtgData`: Pydantic model representing a single ARTG entry with fields like ARTG ID, name, active ingredients, dosage form, sponsor info, shortage status, and dates
- `ArtgResults`: Root model containing a list of ArtgData entries
- Custom date validation that parses DD/MM/YYYY format dates from the TGA CSV

#### CLI Interface (`tga_shortage_scraper/__main__.py`)
- Click-based command line interface with optional `--ingredient` filter
- Makes HTTP requests to `https://apps.tga.gov.au/Prod/msi/search`
- Handles CSV response parsing and skips TGA headers (first 10 lines)
- Outputs structured JSON with proper error handling

#### Data Processing Flow
1. Constructs API parameters for "All" shortage types and "Excel" export format
2. Fetches CSV data from TGA endpoint  
3. Skips first 10 lines (Excel headers and TGA metadata)
4. Parses remaining CSV into ArtgData objects
5. Optionally filters by ingredient name (searches both active ingredients and ARTG name)
6. Outputs as formatted JSON

### Key Technical Details
- Uses `requests.Session()` for HTTP requests
- Handles BrokenPipeError for piped output scenarios
- Date fields are optional and converted from DD/MM/YYYY strings to Python date objects
- Ingredient filtering is case-insensitive and searches both active ingredients and ARTG name fields
- Uses uv for Python package management
- Follows strict typing with mypy --strict