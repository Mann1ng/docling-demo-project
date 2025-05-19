from pdf_to_text import convert_pdf_to_hierarchical_text
import os

def main():
    """
    Demonstrate how to use the convert_pdf_to_hierarchical_text function.
    """
    # Example 1: Convert a PDF from a URL
    print("Example 1: Converting a PDF from a URL")
    url = "https://arxiv.org/pdf/2408.09869"
    try:
        text = convert_pdf_to_hierarchical_text(
            source=url,
            max_pages=5  # Only process first 5 pages
        )
        print(f"Successfully converted PDF from URL. First 500 chars:")
        print(text[:500] + "...\n")
    except Exception as e:
        print(f"Error converting PDF from URL: {e}\n")

    # Example 2: Convert a local PDF file (if available)
    print("Example 2: Converting a local PDF file")
    local_file = input("Enter path to a local PDF file (or press Enter to skip): ")
    if local_file and os.path.exists(local_file):
        try:
            text = convert_pdf_to_hierarchical_text(
                source=local_file,
                output_format="markdown",
                accurate_tables=True
            )
            # Save to file
            output_file = os.path.splitext(local_file)[0] + ".md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Successfully converted local PDF to {output_file}")
        except Exception as e:
            print(f"Error converting local PDF: {e}\n")
    else:
        print("Skipping local file example.\n")

    # Example 3: Convert with binary data
    print("Example 3: Converting a PDF from binary data (simulated)")
    print("In a real application, this could come from an API response or a database blob")
    try:
        # Simulate binary data - in real use, this would come from elsewhere
        if local_file and os.path.exists(local_file):
            with open(local_file, "rb") as f:
                binary_data = f.read()
            
            text = convert_pdf_to_hierarchical_text(
                source=binary_data,
                output_format="json"  # Get JSON format this time
            )
            print(f"Successfully converted binary data. Result type: {type(text)}")
            print(f"JSON output (first 300 chars): {text[:300]}...\n")
        else:
            print("Skipping binary example - no local file available.\n")
    except Exception as e:
        print(f"Error converting binary data: {e}\n")

if __name__ == "__main__":
    main() 