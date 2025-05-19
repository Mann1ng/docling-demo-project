#!/usr/bin/env python3
"""
Extract hierarchical structure from a PDF document and output as JSON.
This preserves document structure including headings, lists, and tables.
"""

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.datamodel.base_models import InputFormat, DocumentStream
from typing import Union, Optional, BinaryIO, Dict, Any
from pathlib import Path
import json
import argparse
import os
import sys


def convert_pdf_to_hierarchical_json(
    source: Union[str, Path, BinaryIO, bytes],
    output_file: Optional[str] = None,
    max_pages: Optional[int] = None,
    max_file_size: Optional[int] = None,
    accurate_tables: bool = True,
    pretty_print: bool = True,
    artifacts_path: Optional[str] = None,
    enable_remote_services: bool = False,
    print_summary: bool = False
) -> Dict[str, Any]:
    """
    Convert a PDF document to hierarchical JSON structure.
    
    Args:
        source: PDF source - can be a file path, URL, binary stream, or bytes
        output_file: Optional path to save the JSON output
        max_pages: Maximum number of pages to process
        max_file_size: Maximum file size in bytes
        accurate_tables: Use accurate table extraction (slower but better quality)
        pretty_print: Whether to format the JSON with indentation
        artifacts_path: Path to pre-downloaded models (optional)
        enable_remote_services: Allow communication with remote services
        print_summary: Whether to print a summary of the document structure
        
    Returns:
        Dictionary containing the hierarchical representation of the document
    """
    # Configure pipeline options
    pipeline_options = PdfPipelineOptions(
        do_table_structure=True,
        artifacts_path=artifacts_path,
        enable_remote_services=enable_remote_services
    )
    
    # Set table extraction mode
    if accurate_tables:
        pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
    else:
        pipeline_options.table_structure_options.mode = TableFormerMode.FAST
    
    # Create the converter with options
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    
    # Prepare conversion arguments
    convert_args = {}
    if max_pages is not None:
        convert_args["max_num_pages"] = max_pages
    if max_file_size is not None:
        convert_args["max_file_size"] = max_file_size
    
    # Convert the document
    result = converter.convert(source, **convert_args)
    
    # Get JSON structure - this preserves document hierarchy
    if output_file:
        # If we're saving to a file, use save_as_json method
        indent = 2 if pretty_print else None
        result.document.save_as_json(output_file, indent=indent)
        print(f"Hierarchical JSON output saved to {output_file}")
    
    # Get the document as a Python dictionary
    doc_dict = result.document.model_dump()
    
    # Print summary if requested
    if print_summary:
        print_document_summary(doc_dict)
    
    return doc_dict


def print_document_summary(doc: Dict[str, Any]) -> None:
    """
    Print a summary of the document's structure.
    
    Args:
        doc: The document dictionary
    """
    print("\nDocument Summary:")
    print(f"  Name: {doc.get('name', 'Unknown')}")
    print(f"  Version: {doc.get('version', 'Unknown')}")
    
    # Count pages
    pages = doc.get('pages', {})
    if isinstance(pages, dict):
        print(f"  Pages: {len(pages)}")
    elif isinstance(pages, list):
        print(f"  Pages: {len(pages)}")
    
    # Count different element types
    print(f"  Text blocks: {len(doc.get('texts', []))}")
    print(f"  Tables: {len(doc.get('tables', []))}")
    print(f"  Pictures: {len(doc.get('pictures', []))}")
    print(f"  Groups: {len(doc.get('groups', []))}")
    
    # Print sample document structure
    print("\nDocument Structure:")
    
    # Find headings and section titles in text blocks
    headings = []
    for text in doc.get('texts', []):
        # Look for headings based on type, label, or text characteristics
        if (text.get('label') == 'heading' or 
            text.get('type') == 'heading' or
            (text.get('text', '').strip().startswith('#') and len(text.get('text', '').strip()) < 100) or
            (text.get('text', '').strip().upper() == text.get('text', '').strip() and len(text.get('text', '').strip()) < 100)):
            
            heading_text = text.get('text', '').strip()
            if heading_text:
                headings.append(heading_text[:80] + ('...' if len(heading_text) > 80 else ''))
    
    print(f"  Found {len(headings)} potential headings/titles")
    for i, heading in enumerate(headings[:5]):  # Show max 5 headings
        print(f"    {i+1}. {heading}")
    if len(headings) > 5:
        print(f"    ... and {len(headings) - 5} more")
    
    # Find tables with dimensions
    if doc.get('tables'):
        print("\nTable Information:")
        for i, table in enumerate(doc.get('tables', [])[:3]):  # Show max 3 tables
            # Try different ways to get table dimensions
            rows = len(table.get('rows', []))
            if 'data' in table and isinstance(table['data'], dict) and 'cells' in table['data']:
                # If using data.cells format
                cells = table['data']['cells']
                if cells:
                    max_row = max([cell.get('row', 0) for cell in cells], default=0) + 1
                    max_col = max([cell.get('col', 0) for cell in cells], default=0) + 1
                    print(f"  Table {i+1}: ~{max_row} rows x ~{max_col} columns")
                else:
                    print(f"  Table {i+1}: Dimensions unknown (no cells found)")
            elif rows > 0:
                # If using rows format
                cols = 0
                if 'cells' in table['rows'][0]:
                    cols = len(table['rows'][0]['cells'])
                print(f"  Table {i+1}: {rows} rows x {cols} columns")
            else:
                print(f"  Table {i+1}: Dimensions unknown")
            
            # Try to show table title/caption if available
            if 'captions' in table and table['captions']:
                caption = table['captions'][0].get('text', '') if isinstance(table['captions'], list) else ''
                if caption:
                    print(f"    Caption: {caption[:80]}..." if len(caption) > 80 else caption)
            
            if i >= 2:  # Only show first 3 tables
                break
        
        if len(doc.get('tables', [])) > 3:
            print(f"    ... and {len(doc.get('tables', [])) - 3} more tables")
    
    print("\nJSON export contains complete hierarchical structure of the document.")


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF documents to hierarchical JSON structure"
    )
    parser.add_argument(
        "source", 
        help="Path or URL to the PDF document"
    )
    parser.add_argument(
        "--output", "-o", 
        help="Path to save the JSON output (default: source_filename.json)"
    )
    parser.add_argument(
        "--max-pages", "-p", 
        type=int, 
        help="Maximum number of pages to process"
    )
    parser.add_argument(
        "--max-file-size", "-s", 
        type=int, 
        help="Maximum file size in bytes"
    )
    parser.add_argument(
        "--fast-tables", 
        action="store_true", 
        help="Use faster but less accurate table extraction"
    )
    parser.add_argument(
        "--no-pretty", 
        action="store_true", 
        help="Output compact JSON without indentation"
    )
    parser.add_argument(
        "--artifacts-path", 
        help="Path to pre-downloaded models"
    )
    parser.add_argument(
        "--enable-remote", 
        action="store_true", 
        help="Allow communication with remote services"
    )
    parser.add_argument(
        "--summary", 
        action="store_true", 
        help="Print a summary of the document structure"
    )
    
    args = parser.parse_args()
    
    # Default output file is source filename with .json extension
    if not args.output:
        source_path = Path(args.source)
        if str(source_path).startswith(("http://", "https://")):
            args.output = "document.json"
        else:
            args.output = str(source_path.with_suffix('.json'))
    
    try:
        convert_pdf_to_hierarchical_json(
            source=args.source,
            output_file=args.output,
            max_pages=args.max_pages,
            max_file_size=args.max_file_size,
            accurate_tables=not args.fast_tables,
            pretty_print=not args.no_pretty,
            artifacts_path=args.artifacts_path,
            enable_remote_services=args.enable_remote,
            print_summary=args.summary
        )
    except Exception as e:
        print(f"Error converting PDF to JSON: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 