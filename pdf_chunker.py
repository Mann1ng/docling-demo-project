from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from typing import Union, Optional, List, Dict, Iterator, Any
from pathlib import Path
import json


def chunk_pdf_document(
    source: Union[str, Path],
    output_json_path: Optional[str] = None,
    tokenizer: str = "BAAI/bge-small-en-v1.5",
    max_pages: Optional[int] = None,
    max_chunk_length: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Convert a PDF to a Docling document and then chunk it into semantic units.
    
    Args:
        source: Path or URL to a PDF document
        output_json_path: Optional path to save the chunks as JSON
        tokenizer: Tokenizer model to use for chunking
        max_pages: Maximum number of pages to process
        max_chunk_length: Maximum text length for each chunk
        
    Returns:
        List of document chunks, each containing text and metadata
    """
    # First convert the document
    print(f"Converting document: {source}")
    
    # Prepare conversion arguments
    convert_args = {}
    if max_pages is not None:
        convert_args["max_num_pages"] = max_pages
    
    conv_result = DocumentConverter().convert(source, **convert_args)
    document = conv_result.document
    
    # Create a chunker with the specified tokenizer
    print(f"Chunking document with tokenizer: {tokenizer}")
    chunker = HybridChunker(tokenizer=tokenizer)
    
    if max_chunk_length:
        chunker.max_chunk_length = max_chunk_length
    
    # Perform chunking
    chunk_iterator = chunker.chunk(document)
    
    # Convert the iterator to a list of chunks
    chunks = list(chunk_iterator)
    print(f"Document chunked into {len(chunks)} segments")
    
    # Save chunks to JSON file if requested
    if output_json_path:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        print(f"Chunks saved to {output_json_path}")
    
    return chunks


def analyze_chunks(chunks: List[Dict[str, Any]]) -> None:
    """
    Print some analysis of the generated chunks.
    
    Args:
        chunks: List of document chunks
    """
    if not chunks:
        print("No chunks to analyze")
        return
    
    # Calculate basic statistics
    text_lengths = [len(chunk["text"]) for chunk in chunks]
    avg_length = sum(text_lengths) / len(text_lengths)
    max_length = max(text_lengths)
    min_length = min(text_lengths)
    
    print("\nChunk Analysis:")
    print(f"Number of chunks: {len(chunks)}")
    print(f"Average chunk length: {avg_length:.1f} characters")
    print(f"Minimum chunk length: {min_length} characters")
    print(f"Maximum chunk length: {max_length} characters")
    
    # Sample of first chunk
    if chunks:
        print("\nSample chunk:")
        first_chunk = chunks[0]
        print(f"Text: {first_chunk['text'][:200]}...")
        
        if "meta" in first_chunk and "headings" in first_chunk["meta"]:
            print(f"Headings: {first_chunk['meta']['headings']}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Chunk a PDF document into semantic units")
    parser.add_argument("source", help="Path or URL to a PDF document")
    parser.add_argument("--output", "-o", help="Path to save chunks as JSON")
    parser.add_argument("--tokenizer", "-t", default="BAAI/bge-small-en-v1.5", 
                        help="Tokenizer model to use for chunking")
    parser.add_argument("--max-pages", "-p", type=int, help="Maximum pages to process")
    parser.add_argument("--max-chunk-length", "-c", type=int, help="Maximum chunk length")
    
    args = parser.parse_args()
    
    chunks = chunk_pdf_document(
        source=args.source,
        output_json_path=args.output,
        tokenizer=args.tokenizer,
        max_pages=args.max_pages,
        max_chunk_length=args.max_chunk_length
    )
    
    analyze_chunks(chunks) 