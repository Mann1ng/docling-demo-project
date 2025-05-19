#!/usr/bin/env python3
"""
Combined example demonstrating PDF processing with Docling:
1. Convert a PDF to hierarchical text
2. Chunk the document into semantic units
3. Perform simple analysis on the results
"""

from pdf_to_text import convert_pdf_to_hierarchical_text
from pdf_chunker import chunk_pdf_document, analyze_chunks
import os
import argparse
import sys
from pathlib import Path


def process_pdf_document(
    source_path: str,
    output_dir: str = None,
    max_pages: int = None,
    do_chunking: bool = True,
    tokenizer: str = "BAAI/bge-small-en-v1.5",
    output_format: str = "markdown"
) -> None:
    """
    Process a PDF document by converting it to text and optionally chunking it.
    
    Args:
        source_path: Path or URL to the PDF document
        output_dir: Directory to save output files (will be created if it doesn't exist)
        max_pages: Maximum number of pages to process
        do_chunking: Whether to perform document chunking
        tokenizer: Tokenizer model to use for chunking
        output_format: Format for hierarchical text output ('markdown' or 'json')
    """
    # Create output directory if needed
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    else:
        # Use default output directory
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
    
    # Generate base filename from source
    if source_path.startswith(("http://", "https://")):
        # Extract filename from URL
        base_filename = source_path.split("/")[-1].split(".")[0]
    else:
        # Extract filename from local path
        base_filename = Path(source_path).stem
    
    print(f"\n{'='*80}")
    print(f"Processing document: {source_path}")
    print(f"{'='*80}")
    
    # Step 1: Convert to hierarchical text
    print("\n[Step 1] Converting PDF to hierarchical text...")
    try:
        hierarchical_text = convert_pdf_to_hierarchical_text(
            source=source_path,
            output_format=output_format,
            max_pages=max_pages,
            accurate_tables=True
        )
        
        # Save the output
        output_extension = ".md" if output_format == "markdown" else ".json"
        output_path = os.path.join(output_dir, f"{base_filename}{output_extension}")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(hierarchical_text)
        
        print(f"Hierarchical text saved to: {output_path}")
        print(f"Text preview (first 500 chars):")
        print(f"{hierarchical_text[:500]}...")
        
    except Exception as e:
        print(f"Error converting document: {e}")
        return
    
    # Step 2: Chunk the document (optional)
    if do_chunking:
        print("\n[Step 2] Chunking document into semantic units...")
        try:
            chunks_output_path = os.path.join(output_dir, f"{base_filename}_chunks.json")
            chunks = chunk_pdf_document(
                source=source_path,
                output_json_path=chunks_output_path,
                tokenizer=tokenizer,
                max_pages=max_pages
            )
            
            # Analyze the chunks
            analyze_chunks(chunks)
            
        except Exception as e:
            print(f"Error chunking document: {e}")
    
    print(f"\n{'='*80}")
    print("Processing complete!")
    print(f"{'='*80}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a PDF document with Docling")
    parser.add_argument("source", help="Path or URL to a PDF document")
    parser.add_argument("--output-dir", "-o", help="Directory to save output files")
    parser.add_argument("--max-pages", "-p", type=int, help="Maximum pages to process")
    parser.add_argument("--no-chunking", action="store_true", help="Skip document chunking")
    parser.add_argument("--tokenizer", "-t", default="BAAI/bge-small-en-v1.5", help="Tokenizer for chunking")
    parser.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown", 
                       help="Output format for hierarchical text")
    
    args = parser.parse_args()
    
    process_pdf_document(
        source_path=args.source,
        output_dir=args.output_dir,
        max_pages=args.max_pages,
        do_chunking=not args.no_chunking,
        tokenizer=args.tokenizer,
        output_format=args.format
    ) 