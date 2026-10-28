import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def parse_menu_items(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Grab MENU array block
    match = re.search(r'export const MENU:\s*MenuItem\[\]\s*=\s*\[([\s\S]*?)\];', text)
    if not match:
        print(f"No MENU found in {path}")
        return []
    
    body = match.group(1)
    # Split into objects
    item_blocks = re.findall(r'\{([^{}]*?)\}', body)
    items = []
    for b in item_blocks:
        obj = {}
        # Find key: val patterns separated by comma or newline
        pairs = re.findall(r'(\w+):\s*([^,}\n]+)', b)
        for key, val in pairs:
            val = val.strip()
            if val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            elif val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.isdigit():
                val = int(val)
            elif val in ('true', 'false'):
                val = (val == 'true')
            obj[key] = val
        if 'id' in obj and 'name' in obj:
            items.append(obj)
    return items

p_7a = r"c:\Users\pc\Desktop\mô hình quán ăn nhanh\src\lib\store.ts"
p_ct = r"c:\Users\pc\Desktop\Plan\com-tam-suon-nuong-app\src\lib\store.ts"
p_cf = r"c:\Users\pc\Desktop\cafe-an-vat-tram-khoi-nghiep\src\lib\store.ts"

m_7a = parse_menu_items(p_7a)
m_ct = parse_menu_items(p_ct)
m_cf = parse_menu_items(p_cf)

print(f"7A items: {len(m_7a)}")
print(f"Com Tam items: {len(m_ct)}")
print(f"Cafe items: {len(m_cf)}")

catalog = {
    "store_7a": m_7a,
    "store_comtam": m_ct,
    "store_cafe": m_cf,
    "total_dishes": len(m_7a) + len(m_ct) + len(m_cf),
    "updated_at": "2026-10-29T00:05:00+07:00"
}

out_path = r"c:\Users\pc\Desktop\Cong viec\AI_Virtual_Office_247\menu_catalog.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print("Updated menu_catalog.json successfully!")
