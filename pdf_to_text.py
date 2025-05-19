from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.datamodel.base_models import InputFormat, DocumentStream
from io import BytesIO
from typing import Union, Optional, BinaryIO
import os
from pathlib import Path


def convert_pdf_to_hierarchical_text(
    source: Union[str, Path, BinaryIO, bytes],
    output_format: str = "markdown",
    max_pages: Optional[int] = None,
    max_file_size: Optional[int] = None,
    accurate_tables: bool = True,
    artifacts_path: Optional[str] = None,
    enable_remote_services: bool = False
) -> str:
    """
    Convert a PDF document to hierarchical text.
    
    Args:
        source: PDF source - can be a file path, URL, binary stream, or bytes
        output_format: Output format, either 'markdown' or 'json'
        max_pages: Maximum number of pages to process
        max_file_size: Maximum file size in bytes
        accurate_tables: Use accurate table extraction (slower but better quality)
        artifacts_path: Path to pre-downloaded models (optional)
        enable_remote_services: Allow communication with remote services
        
    Returns:
        String containing the hierarchical text representation of the document
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
    
    # Handle different source types
    if isinstance(source, bytes):
        source = DocumentStream(name="document.pdf", stream=BytesIO(source))
    elif hasattr(source, 'read') and callable(source.read):  # File-like object
        source = DocumentStream(name="document.pdf", stream=source)
    # String or Path will be handled automatically by convert()
    
    # Prepare conversion arguments
    convert_args = {}
    if max_pages is not None:
        convert_args["max_num_pages"] = max_pages
    if max_file_size is not None:
        convert_args["max_file_size"] = max_file_size
    
    # Convert the document
    result = converter.convert(source, **convert_args)
    
    # Export in the requested format
    if output_format.lower() == "json":
        return result.document.to_json()
    else:  # Default to markdown
        return result.document.export_to_markdown()


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        try:
            hierarchical_text = convert_pdf_to_hierarchical_text(pdf_path)
            print(hierarchical_text)
            
            # Optionally save to file
            output_path = pdf_path.rsplit(".", 1)[0] + ".md"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(hierarchical_text)
            print(f"Output saved to {output_path}")
            
        except Exception as e:
            print(f"Error converting PDF: {str(e)}")
    else:
        print("Usage: python pdf_to_text.py <pdf_path_or_url>") 