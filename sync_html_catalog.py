import json
import re

with open(r'c:\Users\pc\Desktop\Cong viec\AI_Virtual_Office_247\menu_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

# Ensure key is store_cafe_anvat
if 'store_cafe' in cat and 'store_cafe_anvat' not in cat:
    cat['store_cafe_anvat'] = cat.pop('store_cafe')

# Re-save menu_catalog.json
with open(r'c:\Users\pc\Desktop\Cong viec\AI_Virtual_Office_247\menu_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(cat, f, ensure_ascii=False, indent=2)

cat_json_str = json.dumps(cat, ensure_ascii=False, indent=2)

with open(r'c:\Users\pc\Desktop\Cong viec\AI_Virtual_Office_247\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace EMBEDDED_MENU_CATALOG = { ... };
pattern = r'const EMBEDDED_MENU_CATALOG\s*=\s*\{[\s\S]*?\n\s*\};'
replacement = f'const EMBEDDED_MENU_CATALOG = {cat_json_str};'

new_html, count = re.subn(pattern, replacement, html, count=1)
if count == 1:
    with open(r'c:\Users\pc\Desktop\Cong viec\AI_Virtual_Office_247\index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Successfully updated EMBEDDED_MENU_CATALOG in index.html!")
else:
    print(f"Failed to replace EMBEDDED_MENU_CATALOG, matches={count}")
