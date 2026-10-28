import os
import sys
import shutil
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

# 1. Base Paths
BASE_7A = r"c:\Users\pc\Desktop\mô hình quán ăn nhanh"
MENU_7A = os.path.join(BASE_7A, "menu")
PUB_7A = os.path.join(BASE_7A, "public", "menu")

BASE_CAFE = r"c:\Users\pc\Desktop\cafe-an-vat-tram-khoi-nghiep"
PUB_CAFE = os.path.join(BASE_CAFE, "public", "menu")

BASE_COMTAM = r"c:\Users\pc\Desktop\Plan\com-tam-suon-nuong-app"
PUB_COMTAM = os.path.join(BASE_COMTAM, "public", "menu")

BASE_OFFICE = r"c:\Users\pc\Desktop\Cong viec\AI_Virtual_Office_247"
PUB_OFFICE_7A = os.path.join(BASE_OFFICE, "menu_7a")
PUB_OFFICE_CAFE = os.path.join(BASE_OFFICE, "menu_cafe")
PUB_OFFICE_COMTAM = os.path.join(BASE_OFFICE, "menu_comtam")

for d in [PUB_7A, PUB_CAFE, PUB_COMTAM, PUB_OFFICE_7A, PUB_OFFICE_CAFE, PUB_OFFICE_COMTAM]:
    os.makedirs(d, exist_ok=True)

def crop_and_save(src_path, dst_path, target_size=(700, 700), crop_box=None):
    with Image.open(src_path) as im:
        im = im.convert("RGB")
        if crop_box:
            im = im.crop(crop_box)
        w, h = im.size
        # Center-crop to square
        if w > h:
            left = (w - h) // 2
            im = im.crop((left, 0, left + h, h))
        elif h > w:
            top = (h - w) // 2
            im = im.crop((0, top, w, top + w))
        im = im.resize(target_size, Image.Resampling.LANCZOS)
        im.save(dst_path, "JPEG", quality=92)
        print(f"Processed -> {dst_path} ({target_size})")

# ==========================================
# PART 1: QUÁN ĂN NHANH 7A
# ==========================================
print("=== Processing Quán 7A ===")

# Decal BBK items
decal_path = os.path.join(MENU_7A, "1792899798876_5916925786758833898_5916925786758833898_8c4602dcb863bf04da784e3fe5b4cd10.jpg")
if os.path.exists(decal_path):
    with Image.open(decal_path) as im:
        w, h = im.size
        bbk_crops = {
            "bbk-1.jpg": (int(w * 0.45), int(h * 0.726), int(w * 0.62), int(h * 0.888)),
            "bbk-2.jpg": (int(w * 0.45), int(h * 0.562), int(w * 0.62), int(h * 0.722)),
            "bbk-3.jpg": (int(w * 0.62), int(h * 0.562), int(w * 0.785), int(h * 0.722)),
            "bbk-4.jpg": (int(w * 0.795), int(h * 0.562), int(w * 0.96), int(h * 0.722)),
            "bbk-5.jpg": (int(w * 0.62), int(h * 0.726), int(w * 0.785), int(h * 0.888)),
        }
        for fname, box in bbk_crops.items():
            crop_and_save(decal_path, os.path.join(PUB_7A, fname), crop_box=box)

# 4 Original Food Photos
map_orig_7a = {
    "1792899802621_5916925786758833898_5916925786758833898_98bd1798385a8e9f9ead925f818c7131.jpg": "com-2.jpg", # Cơm Gà Xối Mỡ
    "1792899808719_5916925786758833898_5916925786758833898_652ff7cc01d7e240857182841c97bbbf.jpg": "com-3.jpg", # Cơm Gà Chiên Mắm Tỏi
    "1792899812325_5916925786758833898_5916925786758833898_7e8861f8c0c1e37f0e5f5c6e08049e90.jpg": "mi-1.jpg",  # Mì Xào Hải Sản
    "1792899805683_5916925786758833898_5916925786758833898_14458dcfb950458a185288180e43ed7b.jpg": "mi-3.jpg",  # Mì Xào Giòn
}
for src, dst in map_orig_7a.items():
    sp = os.path.join(MENU_7A, src)
    if os.path.exists(sp):
        crop_and_save(sp, os.path.join(PUB_7A, dst))

# 14 New Scanned / Real Dish Photos
map_new_7a = {
    "1793205509243_5916925786758833898_5916925786758833898_f88163deb0aab8c71ca9b97aab90e3f3.jpg": "com-4.jpg", # Cơm Chiên Hải Sản
    "1793205509310_5916925786758833898_5916925786758833898_2047676aa2f7817b234b6170f179be8f.jpg": "com-5.jpg", # Mực Xào Thập Cẩm (Cơm Xào)
    "1793205509395_5916925786758833898_5916925786758833898_918790f5019cda3385a7bd9273fa11e3.jpg": "com-6.jpg", # Bò Lúc Lắc (Cơm Bò Lúc Lắc)
    "1793205509331_5916925786758833898_5916925786758833898_0682c6c0ea52a8f8184fe36db48f26ac.jpg": "com-7.jpg", # Cơm Chiên Trứng + Bò Xào Củ Hành
    "1793205509374_5916925786758833898_5916925786758833898_5eea67831ceadc66c7be9fa307a5dd7e.jpg": "com-8.jpg", # Bò Xào Củ Hành Lót Xà Lách Dầu Giấm
    "1793205509287_5916925786758833898_5916925786758833898_d2e093dcbdf8569ab69a6f4dc3f02fca.jpg": "mi-2.jpg",  # Mì Xào Bò Có Trứng
    "1793205509265_5916925786758833898_5916925786758833898_c7c331241388f9717633490e67c20e43.jpg": "mi-4.jpg",  # Nui Xào Bò Có Trứng
    "1793205509443_5916925786758833898_5916925786758833898_cf89558d4aa4295ac33fd617c4542b0d.jpg": "mi-5.jpg",  # Mì Ý Sốt Bò Bằm
    "1793205509467_5916925786758833898_5916925786758833898_68b10f33b48b0077a137b9ba41531b4c.jpg": "ff-1.jpg",  # Bánh Mì Bò Né Thập Cẩm (Chảo Gang)
    "1793205509489_5916925786758833898_5916925786758833898_14ad9b58b65c04ccea32d9b986ffc140.jpg": "ff-2.jpg",  # Bánh Mì Nướng Bơ Tỏi Phô Mai
    "1793205509419_5916925786758833898_5916925786758833898_474197de7eb1b8f46fb9eaf252be98a6.jpg": "ff-3.jpg",  # Bò Bít Tết Khoai Tây Chiên
    "1793205509352_5916925786758833898_5916925786758833898_833509fed19be0c5d88332c1a73a7165.jpg": "ff-4.jpg",  # Mì Cay HQ Thập Cẩm
    "1793205509511_5916925786758833898_5916925786758833898_d80e87e2562814e1a6bc01eb071b6ffb.jpg": "ff-5.jpg",  # Khoai Tây Lắc Phô Mai
}
for src, dst in map_new_7a.items():
    sp = os.path.join(MENU_7A, src)
    if os.path.exists(sp):
        crop_and_save(sp, os.path.join(PUB_7A, dst))

# Also copy com-1 and toppings
extra_7a = {
    "Com_Chien_Phu_Trung.jpg": "com-1.jpg",
    "Trung_Op_La_Them.jpg": "tp-1.jpg",
    "Pho_Mai_Lat_Them.jpg": "tp-2.jpg",
    "Sandwich_Kep_Trung_Xuc_Xich.jpg": "tp-3.jpg", # Bánh Mì Thêm
    "Com_Them_Vat_Mi_Them.jpg": "tp-4.jpg",
    "Pepsi_Coca_7Up_Tra_Da.jpg": "tp-5.jpg"
}
for src, dst in extra_7a.items():
    sp = os.path.join(MENU_7A, src)
    if os.path.exists(sp):
        crop_and_save(sp, os.path.join(PUB_7A, dst))

# ==========================================
# PART 2: QUÁN CƠM TẤM SƯỜN NƯỚNG
# ==========================================
print("=== Processing Quán Cơm Tấm ===")

banner_4k = r"c:\Users\pc\Desktop\Plan\File_In_An_4K\Bang_Dung_Hop_Den_1m2x2m_4K.jpg"
if os.path.exists(banner_4k):
    with Image.open(banner_4k) as im:
        w, h = im.size
        plate = im.crop((int(w * 0.02), int(h * 0.485), int(w * 0.98), int(h * 0.785)))
        pw, ph = plate.size
        cx = pw // 2
        crop_w = int(ph * 1.05)
        plate_sq = plate.crop((max(0, cx - crop_w // 2), 0, min(pw, cx + crop_w // 2), ph))
        plate_sq = plate_sq.resize((700, 700), Image.Resampling.LANCZOS)
        plate_sq.save(os.path.join(PUB_COMTAM, "ct-1.jpg"), "JPEG", quality=92)
        plate_sq.save(os.path.join(PUB_COMTAM, "ct-2.jpg"), "JPEG", quality=92)
        plate_sq.save(os.path.join(PUB_COMTAM, "ct-3.jpg"), "JPEG", quality=92)
        plate_sq.save(os.path.join(PUB_COMTAM, "ct-4.jpg"), "JPEG", quality=92)
        plate_sq.save(os.path.join(PUB_COMTAM, "ct-5.jpg"), "JPEG", quality=92)
        plate_sq.save(os.path.join(PUB_COMTAM, "ct-6.jpg"), "JPEG", quality=92)
        plate_sq.save(os.path.join(PUB_COMTAM, "ct-7.jpg"), "JPEG", quality=92)
        print("Updated ct-1 to ct-7 from 4K Banner plate")

# Copy the real Cơm Chiên Hải Sản and Bò Xào into Com Tam
shutil.copy2(os.path.join(PUB_7A, "com-4.jpg"), os.path.join(PUB_COMTAM, "cc-3.jpg"))
shutil.copy2(os.path.join(PUB_7A, "com-7.jpg"), os.path.join(PUB_COMTAM, "cc-1.jpg"))

# ==========================================
# PART 3: QUÁN CAFE ĂN VẶT ĐÔNG THẠNH
# ==========================================
print("=== Processing Quán Cafe Ăn Vặt ===")

menu_board = r"c:\Users\pc\Desktop\Plan\menu\Menu_Dung_Khai_Truong.png"
if os.path.exists(menu_board):
    with Image.open(menu_board) as im:
        im = im.convert("RGB")
        # 9 drinks
        drink_crops = {
            "ep-1.jpg": (84, 375, 146, 437),   # Cam Sành Miền Tây
            "ep-2.jpg": (415, 375, 477, 437),  # Nước Ép Dưa Hấu
            "sam-1.jpg": (84, 665, 146, 727),  # Sâm Mía Lau
            "sam-2.jpg": (415, 665, 477, 727), # Sâm Bông Cúc
            "sam-3.jpg": (84, 755, 146, 817),  # Sâm Táo Đỏ Long Nhãn
        }
        for fname, box in drink_crops.items():
            c = im.crop(box)
            c = c.resize((700, 700), Image.Resampling.LANCZOS)
            c.save(os.path.join(PUB_CAFE, fname), "JPEG", quality=92)
            print(f"Updated {fname} from Menu_Dung_Khai_Truong")

# Khoai tây lắc phô mai from real scan
shutil.copy2(os.path.join(PUB_7A, "ff-5.jpg"), os.path.join(PUB_CAFE, "av-2.jpg"))
# BBK items also into Cafe if needed
for i in range(1, 6):
    shutil.copy2(os.path.join(PUB_7A, f"bbk-{i}.jpg"), os.path.join(PUB_CAFE, f"bbk-{i}.jpg"))
# Bò né / Mì cay also into Cafe
shutil.copy2(os.path.join(PUB_7A, "ff-4.jpg"), os.path.join(PUB_CAFE, "mi-1.jpg"))
shutil.copy2(os.path.join(PUB_7A, "mi-2.jpg"), os.path.join(PUB_CAFE, "mi-2.jpg"))
shutil.copy2(os.path.join(PUB_7A, "ff-1.jpg"), os.path.join(PUB_CAFE, "mi-3.jpg"))

# ==========================================
# PART 4: SYNC TO AI VIRTUAL OFFICE 24/7
# ==========================================
print("=== Syncing to Virtual Office ===")

for f in os.listdir(PUB_7A):
    if f.endswith(".jpg"):
        shutil.copy2(os.path.join(PUB_7A, f), os.path.join(PUB_OFFICE_7A, f))

for f in os.listdir(PUB_CAFE):
    if f.endswith(".jpg"):
        shutil.copy2(os.path.join(PUB_CAFE, f), os.path.join(PUB_OFFICE_CAFE, f))

for f in os.listdir(PUB_COMTAM):
    if f.endswith(".jpg"):
        shutil.copy2(os.path.join(PUB_COMTAM, f), os.path.join(PUB_OFFICE_COMTAM, f))

print("=== ALL IMAGES PROCESSED SUCCESSFULLY ===")
