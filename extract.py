import json
import os

input_path = r"c:\Users\Tung\Downloads\Data visualization\crypto_dashboard\Data_visualization.ipynb"
output_path = r"c:\Users\Tung\Downloads\Data visualization\crypto_dashboard\md_cells.json"

try:
    with open(input_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    md_cells = []
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            md_cells.append({'index': i, 'source': cell['source']})
            
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(md_cells, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(md_cells)} markdown cells.")
except Exception as e:
    print(f"Error: {e}")
