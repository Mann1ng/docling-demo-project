import json
import sys
from pathlib import Path

# Load the JSON file
json_path = Path("test_output/sa_rules_hierarchical.json")
with open(json_path, "r", encoding="utf-8") as f:
    doc = json.load(f)

# Print basic document structure
print(f"Document name: {doc['name']}")
print(f"Document version: {doc['version']}")
print(f"Document structure keys: {list(doc.keys())}")

# Print counts of different element types
print(f"Number of text blocks: {len(doc.get('texts', []))}")
print(f"Number of tables: {len(doc.get('tables', []))}")
print(f"Number of pictures: {len(doc.get('pictures', []))}")

# Print information about 'pages'
pages = doc.get('pages', {})
print(f"Pages type: {type(pages)}")
if isinstance(pages, dict):
    print(f"Pages keys: {list(pages.keys())}")
elif isinstance(pages, list):
    print(f"Number of pages: {len(pages)}")

# Print some sample text content
print("\nSample text content:")
for i, text in enumerate(doc.get('texts', [])[:5]):
    if 'text' in text:
        print(f"  Text {i+1}: {text['text'][:100]}...")
    else:
        print(f"  Text {i+1}: {text}")
    if i >= 4:  # Only show first 5 texts
        break

# Print sample table content
if doc.get('tables'):
    print("\nSample table content:")
    table = doc['tables'][0]
    print(f"  Table keys: {list(table.keys())}")
    if 'rows' in table:
        print(f"  Number of rows: {len(table['rows'])}")
        if table['rows'] and 'cells' in table['rows'][0]:
            first_row = table['rows'][0]
            print(f"  First row cells: {len(first_row['cells'])}")
            for i, cell in enumerate(first_row['cells'][:3]):
                if 'text' in cell:
                    print(f"    Cell {i+1}: {cell['text'][:50]}...")
                else:
                    print(f"    Cell {i+1}: {cell}")

print("\nJSON export successful!") 