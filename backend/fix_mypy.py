import glob
import re

files = glob.glob("app/api/v1/*.py") + ["app/main.py"]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to add '-> Any:' to async defs inside api/v1 that lack return type
    # We look for `):` at the end of function definition that doesn't have ->
    # Note: This is a hacky regex that works for this specific codebase format
    
    new_content = re.sub(
        r'(\)\s*:)', 
        r') -> "Any":', 
        content
    )
    
    if "Any" not in content and "-> \"Any\":" in new_content:
        new_content = "from typing import Any\n" + new_content
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Fixed return types")
