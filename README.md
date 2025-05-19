# Docling Demo
## PDF to Structured Text

This is a Python virtual environment with the [docling](https://pypi.org/project/docling/) package installed via:

```
pip install docling
```

## Activating the Environment

```
.\venv\Scripts\Activate.ps1  # PowerShell
```

Or:

```
.\venv\Scripts\activate.bat  # CMD
```

For Linux/Mac:

Note: The current virtual environment is set up for Windows. On Linux/Mac, you'll need to create a new virtual environment first:

```
python -m venv venv
source venv/bin/activate
pip install docling
```

## Available Tools

### PDF to Hierarchical Text Converter

Extracts structured content from PDF documents in Markdown format.

```
python pdf_to_text.py path/to/document.pdf
```

Features:

- Preserves document structure (headings, tables, formatting)
- Supports local files, URLs, and binary data
- Controls for processing parameters (page limits, table accuracy)

### PDF to Hierarchical JSON Converter

Extracts structured content from PDF documents as hierarchical JSON.

```
python pdf_to_json.py path/to/document.pdf [--output output.json] [--summary]
```

Features:

- Preserves document hierarchy (headings, sections, lists, tables)
- Pretty or compact JSON output options
- Command line options for processing control

### PDF Document Chunker

Splits PDF content into semantic chunks for easier processing.

```
python pdf_chunker.py path/to/document.pdf
```

## Using in Your Code

```python
# PDF to Text Example
from pdf_to_text import convert_pdf_to_hierarchical_text

text = convert_pdf_to_hierarchical_text(
    source="document.pdf",
    output_format="markdown",
    max_pages=20,
    accurate_tables=True
)

# PDF to JSON Example
from pdf_to_json import convert_pdf_to_hierarchical_json

json_doc = convert_pdf_to_hierarchical_json(
    source="document.pdf",
    output_file="output.json",
    max_pages=10,
    accurate_tables=True
)
```

## Example Scripts

The repository includes examples showing how to use Docling:

- `example_usage.py` - Basic PDF to text conversion
- `combined_example.py` - Comprehensive PDF processing and chunking

## Package Information

The following docling-related packages are installed:

- docling 2.32.0
- docling-core 2.31.0
- docling-ibm-models 3.4.3
- docling-parse 4.0.1

## Getting Help

For more information, refer to the [official documentation](https://docling-project.github.io/docling/usage/).
