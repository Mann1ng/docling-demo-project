import docling

# Print available modules
print("Available modules in docling:")
print(dir(docling))

# Check for version
try:
    print(f"Docling version: {docling.__version__}")
except AttributeError:
    print("Docling does not have a __version__ attribute")

# Try to import some common modules
try:
    from docling import core
    print("Successfully imported docling.core")
except ImportError as e:
    print(f"Failed to import docling.core: {e}")

try:
    from docling import parse
    print("Successfully imported docling.parse")
except ImportError as e:
    print(f"Failed to import docling.parse: {e}")

try:
    from docling_core import Document
    print("Successfully imported Document from docling_core")
except ImportError as e:
    print(f"Failed to import Document from docling_core: {e}")

# Print information about docling
print("\nDocling package information:")
print(f"docling.__file__: {docling.__file__}")
print(f"docling.__path__: {docling.__path__}") 