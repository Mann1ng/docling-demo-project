import docling_core

print("Available modules in docling_core:")
print(dir(docling_core))

# Check for version
try:
    print(f"docling_core version: {docling_core.__version__}")
except AttributeError:
    print("docling_core does not have a __version__ attribute")

# Print information about docling_core
print("\ndocling_core package information:")
print(f"docling_core.__file__: {docling_core.__file__}")
print(f"docling_core.__path__: {docling_core.__path__}")

# Check for commonly used classes/functions
for name in ["Document", "create_document", "process_document", "TextBlock", "Page"]:
    if hasattr(docling_core, name):
        print(f"docling_core.{name} exists")
    else:
        print(f"docling_core.{name} does not exist") 