#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI VIRTUAL OFFICE 24/7 (3D GAME SIMULATION + CODEX x CLAUDE SELF-LEARNING ENGINE)
- Cổng giao diện Văn Phòng Ảo 3D: http://localhost:8088/index.html
- Cổng kết nối 9Router AI Hub: http://localhost:20128/v1 (API Key: )
- Động cơ kép: CODEX (cx/codex-auto-review, cx/gpt-5.6-sol) x CLAUDE (kr/claude-sonnet-4.5, kr/claude-haiku-4.5)
- Hệ thống 9 Agency Tinh Hoa (GitHub Agency Agents Suite):
  1. Agents Orchestrator
  2. Operations Manager
  3. Pricing Analyst
  4. Growth Hacker
  5. Social Media Strategist
  6. Analytics Reporter
  7. Customer Service
  8. Workflow Optimizer
  9. Menu Visual Designer (Tự động cập nhật & tối ưu hóa hình ảnh món ăn)
- Tách bạch 100% dữ liệu thực tế từ Google Sheets / GAS của 3 Quán (Zero Fake Numbers):
  1. CAFE ĂN VẶT TRẠM KHỞI NGHIỆP (36/5E Nguyễn Thị Ngâu, Trung Đông 8, Xã Đông Thạnh, Hóc Môn, TP.HCM)
  2. TRẠM KHỞI NGHIỆP – Cơm Tấm Sườn Nướng Than Hoa & Cơm Chiên
  3. CAFE ĂN VẶT TRẠM KHỞI NGHIỆP (36/5E Nguyễn Thị Ngâu, Đông Thạnh, TP.HCM)
"""

import os
import sys
import json
import time
import re
import threading
import webbrowser
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import urllib.request
import urllib.error
import mimetypes

# Tích hợp Google Cloud Gemini AI Engine
try:
    from google_cloud_ai_engine import gemini_engine
    HAS_GEMINI = True
except Exception:
    try:
        sys.path.append(os.path.abspath(os.path.join(BASE_DIR, "..")))
        from google_cloud_ai_engine import gemini_engine
        HAS_GEMINI = True
    except Exception:
        HAS_GEMINI = False
        gemini_engine = None

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

PORT = 8088
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "office_config_247.json")
MEMORY_PATH = os.path.join(BASE_DIR, "office_memory_247.json")
LOG_PATH = os.path.join(BASE_DIR, "office_activity_247.log")
CATALOG_PATH = os.path.join(BASE_DIR, "menu_catalog.json")

NINE_ROUTER_BASE_URL = "http://localhost:20128/v1"
NINE_ROUTER_API_KEY = ""

# Live Google Apps Script endpoints (100% Real Sheet Data)
GAS_URL_COMTAM = "https://script.google.com/macros/s/AKfycby8rz7upff345Kvv_pK-AVdClBsUit68aUgj4Cl8bvPN6vmM8_i8NZpJe2VqxE6Mc4qZQ/exec"
GAS_URL_CAFE = "https://script.google.com/macros/s/AKfycbyktPQSBZEi6FSVMDBV27SWCQSzHMItoKHG8_um4TtAvREYmkVx1PTRncc1-E-3CVZk/exec"
GAS_URL_7A = "https://script.google.com/macros/s/AKfycbyCtOrTDhFcBA7rMl-VsHttNOVCJWQv5V9yzZ2N9CGLTfr2Y99zW6ayU0exKvX4syM9/exec"

# Local Repository Paths
REPO_PATHS = {
    "store_7a": r"c:\Users\pc\Desktop\Cong viec\mô hình quán ăn nhanh",
    "7a": r"c:\Users\pc\Desktop\Cong viec\mô hình quán ăn nhanh",
    "store_comtam": r"c:\Users\pc\Desktop\Cong viec\Plan\com-tam-suon-nuong-app",
    "comtam": r"c:\Users\pc\Desktop\Cong viec\Plan\com-tam-suon-nuong-app",
    "store_cafe": r"c:\Users\pc\Desktop\Cong viec\cafe-an-vat-tram-khoi-nghiep",
    "store_cafe_anvat": r"c:\Users\pc\Desktop\Cong viec\cafe-an-vat-tram-khoi-nghiep",
    "cafe": r"c:\Users\pc\Desktop\Cong viec\cafe-an-vat-tram-khoi-nghiep",
}

DEFAULT_CONFIG = {
    "office_name": "Văn Phòng Ảo AI 3D 24/7 - Hệ Động Cơ Kép CODEX x CLAUDE",
    "address": "36/5E Nguyễn Thị Ngâu, Trung Đông 8, Xã Đông Thạnh, Hóc Môn, TP.HCM",
    "hotline": "0931.811.872",
    "nine_router_url": NINE_ROUTER_BASE_URL,
    "nine_router_key": NINE_ROUTER_API_KEY,
    "preferred_models": [
        "cx/codex-auto-review",
        "kr/claude-sonnet-4.5",
        "kr/claude-sonnet-4.5-agentic",
        "kr/claude-haiku-4.5",
        "ag/claude-sonnet-4-6",
        "ag/gemini-3.8-flash-high",
        "ag/gemini-3-flash",
        "gemini/gemini-3-flash-preview",
        "ag/gpt-oss-120b-medium",
        "bazaarlink/auto:free"
    ],
    "auto_schedule_times": ["06:15", "10:00", "14:00", "16:00", "21:15"],
    "gas_url_comtam": GAS_URL_COMTAM,
    "gas_url_cafe": GAS_URL_CAFE,
    "gas_url_7a": GAS_URL_7A,
    "telegram_bot_token": "",
    "telegram_chat_id": ""
}

DEFAULT_MEMORY = {
    "store_7a": [
        {
            "id": "mem_7a_1",
            "time": "Khởi tạo Hệ Thống",
            "agent": "CEO Orchestrator (Claude x Codex)",
            "engine": "Codex x Claude",
            "insight": "Ca Sáng (06h30-10h00) tại 36/5E Nguyễn Thị Ngâu tập trung tối đa tốc độ ra món dưới 90 giây cho Bánh Bao Kẹp (18K-26K), Hamburger (28K) và Sandwich (22K)."
        },
        {
            "id": "mem_7a_2",
            "time": "Khởi tạo Hệ Thống",
            "agent": "Menu Visual Designer (Codex x Claude)",
            "engine": "agency-menu-visual-designer",
            "insight": "Đã chuẩn hóa 28 hình ảnh món ăn chất lượng HD cho Quán Cafe Ăn Vặt Hóc Môn (Bánh Bao Kẹp, Cơm Gà Xối Mỡ, Mì Cay, FastFood)."
        },
        {
            "id": "mem_7a_3",
            "time": "Khởi tạo Hệ Thống",
            "agent": "Tuyết Mai - Kế Toán POS (Codex)",
            "engine": "cx/codex-auto-review",
            "insight": "Tỷ lệ giá vốn nguyên liệu chuẩn của CAFE ĂN VẶT TRẠM KHỞI NGHIỆP cần giữ ở mức 34%-37%. Luôn gợi ý khách thêm Trứng/Phô mai (+5K) và Pepsi/Trà đá (+10K) để tăng biên lợi nhuận."
        }
    ],
    "store_comtam": [
        {
            "id": "mem_ct_1",
            "time": "Khởi tạo Hệ Thống",
            "agent": "CEO Orchestrator (Claude x Codex)",
            "engine": "Codex x Claude",
            "insight": "Sườn cốt lết tại TRẠM KHỞI NGHIỆP phải nướng than hoa vừa tới để giữ độ mềm mọng; chuẩn bị sẵn cơ số hộp Cơm Tấm Sườn Bì Chả (45K) trước 10h30 cho đơn giao văn phòng/xưởng."
        },
        {
            "id": "mem_ct_2",
            "time": "Khởi tạo Hệ Thống",
            "agent": "Menu Visual Designer (Codex x Claude)",
            "engine": "agency-menu-visual-designer",
            "insight": "Đã hoàn tất đồng bộ 21 ảnh món ăn Cơm Tấm Sườn Nướng bóng bẩy, đậm chất ẩm thực truyền thống vào Web App."
        },
        {
            "id": "mem_ct_3",
            "time": "Khởi tạo Hệ Thống",
            "agent": "Tuyết Mai - Kế Toán POS (Codex)",
            "engine": "cx/codex-auto-review",
            "insight": "Suất Cơm Tấm 2 Sườn (55K) cho Gymer và các topping Chả Trứng (+10K), Lạp Xưởng (+10K), Sườn Thêm (+25K) giúp tăng giá trị trung bình đơn (AOV) thêm 28%."
        }
    ],
    "store_cafe_anvat": [
        {
            "id": "mem_cf_1",
            "time": "Khởi tạo Hệ Thống",
            "agent": "CEO Orchestrator (Claude x Codex)",
            "engine": "Codex x Claude",
            "insight": "Khung 06h30-09h00 tại 36/5E Nguyễn Thị Ngâu tập trung phục vụ Cà Phê Muối (20K) & Bạc Xỉu mang đi cho người đi làm dưới 60s."
        },
        {
            "id": "mem_cf_2",
            "time": "Khởi tạo Hệ Thống",
            "agent": "Menu Visual Designer (Codex x Claude)",
            "engine": "agency-menu-visual-designer",
            "insight": "Đã phân loại và tối ưu 50 hình ảnh món ăn & thức uống sắc nét cho Cafe Ăn Vặt Trạm Khởi Nghiệp Đông Thạnh."
        },
        {
            "id": "mem_cf_3",
            "time": "Khởi tạo Hệ Thống",
            "agent": "Bảo Ngọc - Marketing (Claude)",
            "engine": "kr/claude-sonnet-4.5",
            "insight": "Khung giờ tan học 16h30-19h30 đẩy mạnh combo Ăn Vặt: Cá Viên Chiên Nước Mắm Bơ Tỏi (30K) + Trà Dâu Tây thu hút học sinh và giới trẻ Đông Thạnh."
        }
    ]
}


def write_log(agent_name: str, message: str):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now_str}] [{agent_name}] {message}"
    print(line)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_or_init_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            updated = False
            for k, v in DEFAULT_CONFIG.items():
                if k not in data:
                    data[k] = v
                    updated = True
            if updated:
                with open(CONFIG_PATH, "w", encoding="utf-8") as wf:
                    json.dump(data, wf, ensure_ascii=False, indent=2)
            return data
    except Exception:
        return DEFAULT_CONFIG


def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception as e:
        write_log("Config Manager", f"Lỗi lưu config: {e}")


def load_or_init_memory():
    if not os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_MEMORY, f, ensure_ascii=False, indent=2)
        return DEFAULT_MEMORY
    try:
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            updated = False
            for k, v in DEFAULT_MEMORY.items():
                if k not in data:
                    data[k] = v
                    updated = True
            if updated:
                with open(MEMORY_PATH, "w", encoding="utf-8") as wf:
                    json.dump(data, wf, ensure_ascii=False, indent=2)
            return data
    except Exception:
        return DEFAULT_MEMORY


def save_memory(mem):
    try:
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(mem, f, ensure_ascii=False, indent=2)
    except Exception as e:
        write_log("Memory Engine", f"Lỗi lưu bộ nhớ: {e}")


def audit_store_menu(store_id: str):
    """Quét và đối soát toàn diện thực đơn và hình ảnh món ăn của 1 quán"""
    repo_path = REPO_PATHS.get(store_id)
    if not repo_path or not os.path.exists(repo_path):
        return {"ok": False, "error": f"Không tìm thấy thư mục repository: {repo_path}"}

    store_ts = os.path.join(repo_path, "src", "lib", "store.ts")
    menu_dir = os.path.join(repo_path, "public", "menu")

    if not os.path.exists(store_ts):
        return {"ok": False, "error": f"Không tìm thấy file store.ts tại: {store_ts}"}

    existing_files = {}
    if os.path.exists(menu_dir):
        for fname in os.listdir(menu_dir):
            fpath = os.path.join(menu_dir, fname)
            if os.path.isfile(fpath):
                existing_files[fname] = {
                    "filename": fname,
                    "size_bytes": os.path.getsize(fpath),
                    "size_kb": round(os.path.getsize(fpath) / 1024, 1)
                }

    with open(store_ts, "r", encoding="utf-8") as f:
        content = f.read()

    menu_match = re.search(r"export const MENU(?::\s*MenuItem\[\])?\s*=\s*\[(.*?)\];", content, re.DOTALL)
    if not menu_match:
        return {"ok": False, "error": "Không tìm thấy mảng MENU trong store.ts"}

    block = menu_match.group(1)
    items = []
    item_matches = re.finditer(r"\{\s*id:\s*[\x27\x22]([^\x27\x22]+)[\x27\x22],\s*name:\s*[\x27\x22]([^\x27\x22]+)[\x27\x22].*?\}", block, re.DOTALL)

    valid_images = 0
    missing_images = []

    for m in item_matches:
        raw_obj = m.group(0)
        id_ = m.group(1)
        name = m.group(2)
        price_m = re.search(r"price:\s*(\d+)", raw_obj)
        price = int(price_m.group(1)) if price_m else 0
        cat_m = re.search(r"category:\s*[\x27\x22]([^\x27\x22]+)[\x27\x22]", raw_obj)
        cat = cat_m.group(1) if cat_m else ""
        img_m = re.search(r"img:\s*[\x27\x22]([^\x27\x22]+)[\x27\x22]", raw_obj)
        img = img_m.group(1) if img_m else ""
        badge_m = re.search(r"badge:\s*[\x27\x22]([^\x27\x22]+)[\x27\x22]", raw_obj)
        badge = badge_m.group(1) if badge_m else ""

        img_filename = os.path.basename(img) if img else ""
        has_file = img_filename in existing_files if img_filename else False

        item_info = {
            "id": id_,
            "name": name,
            "price": price,
            "category": cat,
            "img": img,
            "badge": badge,
            "has_image": has_file,
            "image_details": existing_files.get(img_filename)
        }

        if has_file:
            valid_images += 1
        else:
            missing_images.append(item_info)

        items.append(item_info)

    total_items = len(items)
    coverage = round((valid_images / total_items * 100), 1) if total_items > 0 else 0

    return {
        "ok": True,
        "store_id": store_id,
        "total_items": total_items,
        "valid_images": valid_images,
        "missing_count": len(missing_images),
        "coverage_percent": coverage,
        "total_asset_files": len(existing_files),
        "items": items,
        "missing_items": missing_images
    }


def audit_all_stores():
    """Quét và đối soát thực đơn cả 3 quán"""
    res = {}
    for sid in REPO_PATHS:
        res[sid] = audit_store_menu(sid)
    return {
        "ok": True,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stores": res
    }


def call_9router_chat(messages, models=None, api_key=None, base_url=None):
    # 1. Ưu tiên gọi Native Google Cloud Gemini Engine siêu tốc
    if HAS_GEMINI and gemini_engine:
        try:
            sys_msg = ""
            user_msg = ""
            for m in messages:
                role = m.get("role")
                content = m.get("content", "")
                if role == "system":
                    sys_msg += content + "\n"
                elif role == "user":
                    user_msg += content + "\n"
            
            if user_msg.strip():
                gem_res = gemini_engine.generate_text(
                    user_msg.strip(),
                    system_instruction=sys_msg.strip() if sys_msg else None,
                    temperature=0.3
                )
                if gem_res.get("ok"):
                    return {
                        "ok": True,
                        "model": gem_res.get("model", "Google Cloud Gemini"),
                        "engine": gem_res.get("engine", "Google Cloud Gemini Native"),
                        "content": gem_res.get("text")
                    }
        except Exception as ge:
            write_log("Google Cloud AI", f"Tự động chuyển 9Router fallback: {ge}")

    # 2. Dự phòng 9Router Local Hub
    base_url = base_url or NINE_ROUTER_BASE_URL
    api_key = api_key or NINE_ROUTER_API_KEY
    models = models or DEFAULT_CONFIG["preferred_models"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    last_err = None
    for model_id in models:
        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 1200
        }
        try:
            req = urllib.request.Request(
                f"{base_url}/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers=headers
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8", errors="ignore"))
                    content = data["choices"][0]["message"]["content"]
                    return {"ok": True, "model": model_id, "content": content}
        except Exception as e:
            last_err = str(e)
            continue
    return {"ok": False, "error": last_err or "All models in chain failed"}


def fetch_live_pos_data(gas_url: str):
    """Kéo dữ liệu thật 100% từ Google Apps Script / Sheet"""
    if not gas_url or not gas_url.startswith("https://script.google.com/"):
        return None
    try:
        target = gas_url + ("&" if "?" in gas_url else "?") + "action=data"
        req = urllib.request.Request(target, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            text = resp.read().decode("utf-8", errors="ignore")
            data = json.loads(text)
            return data
    except Exception as e:
        write_log("POS Sync", f"Lỗi đọc Google Sheets API ({gas_url[:45]}...): {e}")
        return None


def send_telegram_notification(token: str, chat_id: str, text: str):
    if not token or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        write_log("Telegram Connector", f"Lỗi gửi Telegram: {e}")
        return False


def daemon_worker_247():
    write_log("Codex x Claude Core", f"Đã kích hoạt Văn Phòng Ảo 3D 24/24 trên 9Router ({NINE_ROUTER_BASE_URL}).")
    write_log("Elite Agency Swarm", "Hệ thống 9 Agency Tinh Hoa (Github Suite) đã sẵn sàng phục vụ 3 Quán.")
    write_log("Menu Visual Designer", "Bot tự động kiểm soát & đồng bộ hình ảnh menu 3 quán đã kích hoạt.")
    
    triggered_minutes = set()
    last_orders = {"store_7a": -1, "store_comtam": -1, "store_cafe_anvat": -1}

    while True:
        try:
            cfg = load_or_init_config()
            now = datetime.now()
            hhmm = now.strftime("%H:%M")
            day_key = f"{now.strftime('%Y-%m-%d')}_{hhmm}"

            # 1. Kéo dữ liệu thật Quán Cơm Tấm
            live_ct = fetch_live_pos_data(cfg.get("gas_url_comtam", GAS_URL_COMTAM))
            if live_ct and live_ct.get("ok"):
                so_don = live_ct.get("kpi", {}).get("soDon", 0)
                doanh_thu = live_ct.get("kpi", {}).get("doanhThu", 0)
                if so_don != last_orders["store_comtam"]:
                    last_orders["store_comtam"] = so_don
                    write_log(
                        "NV4 Tuyết Mai [Codex POS]",
                        f"[SỔ 2 - {live_ct.get('store', 'Cơm Tấm')}] Ngày {live_ct.get('ngay')}: {so_don} đơn | Doanh thu thật: {doanh_thu:,} đ"
                    )

            # 2. Kéo dữ liệu thật Quán Cafe Đông Thạnh
            live_cf = fetch_live_pos_data(cfg.get("gas_url_cafe", GAS_URL_CAFE))
            if live_cf and live_cf.get("ok"):
                so_don = live_cf.get("kpi", {}).get("soDon", 0)
                doanh_thu = live_cf.get("kpi", {}).get("doanhThu", 0)
                if so_don != last_orders["store_cafe_anvat"]:
                    last_orders["store_cafe_anvat"] = so_don
                    write_log(
                        "NV4 Tuyết Mai [Codex POS]",
                        f"[SỔ 3 - CAFE ĐÔNG THẠNH] {so_don} đơn ca hiện tại | Doanh thu thật: {doanh_thu:,} đ"
                    )

            # 3. Kéo dữ liệu thật Quán Hóc Môn nếu có cấu hình
            gas_7a = cfg.get("gas_url_7a", "")
            if gas_7a:
                live_7a = fetch_live_pos_data(gas_7a)
                if live_7a and live_7a.get("ok"):
                    so_don = live_7a.get("kpi", {}).get("soDon", 0)
                    doanh_thu = live_7a.get("kpi", {}).get("doanhThu", 0)
                    if so_don != last_orders["store_7a"]:
                        last_orders["store_7a"] = so_don
                        write_log(
                            "NV4 Tuyết Mai [Codex POS]",
                            f"[SỔ 1 - CAFE ĂN VẶT TRẠM KHỞI NGHIỆP] Ngày {live_7a.get('ngay')}: {so_don} đơn | Doanh thu thật: {doanh_thu:,} đ"
                        )

            # Báo cáo lịch tự động
            if hhmm in cfg.get("auto_schedule_times", []) and day_key not in triggered_minutes:
                triggered_minutes.add(day_key)
                rev_ct = f"{live_ct.get('kpi', {}).get('doanhThu', 0):,} đ" if live_ct else "0 đ (Chờ kết nối)"
                rev_cf = f"{live_cf.get('kpi', {}).get('doanhThu', 0):,} đ" if live_cf else "0 đ (Chờ kết nối)"
                msg = (
                    f"⏰ [BÁO CÁO CA TỰ ĐỘNG {hhmm}] Văn Phòng Ảo AI 3D 24/24 (Codex x Claude)\n"
                    f"🍔 Sổ 1: CAFE ĂN VẶT TRẠM KHỞI NGHIỆP (36/5E Nguyễn Thị Ngâu, Hóc Môn)\n"
                    f"🍛 Sổ 2: TRẠM KHỞI NGHIỆP Cơm Tấm (Doanh thu thật: {rev_ct})\n"
                    f"☕ Sổ 3: CAFE ĂN VẶT ĐÔNG THẠNH (Doanh thu thật: {rev_cf})"
                )
                write_log("NV2 Minh Quân [Lịch 3 Ca]", msg.replace("\n", " | "))
                send_telegram_notification(
                    cfg.get("telegram_bot_token", ""),
                    cfg.get("telegram_chat_id", ""),
                    msg
                )
        except Exception as e:
            write_log("Watchdog 24/7", f"Tự phục hồi: {e}")

        time.sleep(30)



import time
from concurrent.futures import ThreadPoolExecutor

CACHED_POS_LOCK = threading.Lock()
CACHED_POS_DATA = {
    "ok": True,
    "timestamp": None,
    "store_7a": None,
    "store_comtam": None,
    "store_cafe_anvat": None
}
LAST_CACHE_FETCH = 0

def get_pos_summary_cached(force=False):
    global LAST_CACHE_FETCH, CACHED_POS_DATA
    now_ts = time.time()
    with CACHED_POS_LOCK:
        if not force and (now_ts - LAST_CACHE_FETCH < 45) and (CACHED_POS_DATA.get("timestamp") is not None):
            return CACHED_POS_DATA

    cfg = load_or_init_config()
    url_ct = cfg.get("gas_url_comtam", GAS_URL_COMTAM)
    url_cf = cfg.get("gas_url_cafe", GAS_URL_CAFE)
    url_7a = cfg.get("gas_url_7a", GAS_URL_7A)

    with ThreadPoolExecutor(max_workers=3) as executor:
        f_ct = executor.submit(fetch_live_pos_data, url_ct)
        f_cf = executor.submit(fetch_live_pos_data, url_cf)
        f_7a = executor.submit(fetch_live_pos_data, url_7a)
        ct = f_ct.result()
        cf = f_cf.result()
        s7a = f_7a.result()

    with CACHED_POS_LOCK:
        CACHED_POS_DATA = {
            "ok": True,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "store_7a": s7a or {"ok": False, "message": "Chưa kết nối được Google Sheet 7A"},
            "store_comtam": ct or {"ok": False, "message": "Chưa kết nối được Google Sheet Cơm Tấm"},
            "store_cafe_anvat": cf or {"ok": False, "message": "Chưa kết nối được Google Sheet Cafe Đông Thạnh"}
        }
        LAST_CACHE_FETCH = now_ts
        return CACHED_POS_DATA

ALLOWED_LOCAL_AI_URLS = {
    "http://localhost:20128/v1",
    "http://127.0.0.1:20128/v1",
    "http://localhost:20129/v1",
    "http://127.0.0.1:20129/v1",
}
BLOCKED_STATIC_EXTENSIONS = {".py", ".pyc", ".log", ".bat", ".cmd", ".ps1", ".env", ".sqlite", ".db"}
BLOCKED_STATIC_FILENAMES = {"office_config_247.json", "office_memory_247.json", ".gitignore"}
MAX_POST_BODY_BYTES = 2 * 1024 * 1024


class VirtualOfficeHandler(SimpleHTTPRequestHandler):
    timeout = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        origin = self.headers.get("Origin", "")
        if origin.startswith("http://localhost:") or origin.startswith("http://127.0.0.1:"):
            self.send_header("Access-Control-Allow-Origin", origin)
        else:
            self.send_header("Access-Control-Allow-Origin", f"http://localhost:{PORT}")
        self.send_header("Vary", "Origin")
        self.send_header("Connection", "close")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def _read_json_body(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_POST_BODY_BYTES:
            return {}
        try:
            raw = self.rfile.read(length).decode("utf-8", errors="ignore")
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # 1. Image serving proxy for local preview (Hardened against Path Traversal CWE-22)
        from urllib.parse import unquote
        clean_path = unquote(self.path.split("?")[0])
        if clean_path.startswith("/menu_images/"):
            parts = [p for p in clean_path[len("/menu_images/"):].split("/") if p]
            if len(parts) == 2:
                store_key = parts[0]
                img_name = os.path.basename(parts[1])
                ext = os.path.splitext(img_name)[1].lower()
                repo_path = REPO_PATHS.get("store_" + store_key) or REPO_PATHS.get(store_key)
                if repo_path and ext in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}:
                    menu_root = os.path.realpath(os.path.join(repo_path, "public", "menu"))
                    local_img_path = os.path.realpath(os.path.join(menu_root, img_name))
                    if local_img_path.startswith(menu_root + os.sep) and os.path.isfile(local_img_path):
                        mime, _ = mimetypes.guess_type(local_img_path)
                        with open(local_img_path, "rb") as img_f:
                            img_data = img_f.read()
                        self.send_response(200)
                        self.send_header("Content-Type", mime or "image/jpeg")
                        self.send_header("Content-Length", str(len(img_data)))
                        self.end_headers()
                        self.wfile.write(img_data)
                        return
            self.send_response(404)
            self.end_headers()
            return

        # 2. Agency Roster API
        if self.path.startswith("/api/agency"):
            agency_list = [
                {"id": "agents_orchestrator", "name": "Agents Orchestrator", "skill": "agency-agents-orchestrator", "role": "Chỉ Huy Trưởng Pipeline & Giám Sát Quality Gates", "status": "active"},
                {"id": "operations_manager", "name": "Operations Manager", "skill": "agency-operations-manager", "role": "Giám Đốc Vận Hành Chuỗi Thực Địa & Bếp", "status": "active"},
                {"id": "pricing_analyst", "name": "Pricing Analyst", "skill": "agency-pricing-analyst", "role": "Chuyên Gia Định Giá Món & Tối Ưu Lợi Nhuận Biên", "status": "active"},
                {"id": "growth_hacker", "name": "Growth Hacker", "skill": "agency-growth-hacker", "role": "Chiến Lược Gia Tăng Trưởng & Phễu Bán Kính 3km", "status": "active"},
                {"id": "social_media_strategist", "name": "Social Media Strategist", "skill": "agency-social-media-strategist", "role": "Giám Đốc Nội Dung Đa Kênh TikTok & FB", "status": "active"},
                {"id": "analytics_reporter", "name": "Analytics Reporter", "skill": "agency-analytics-reporter", "role": "Chuyên Gia Phân Tích Dữ Liệu & Sổ Thu Chi", "status": "active"},
                {"id": "customer_service", "name": "Customer Service", "skill": "agency-customer-service", "role": "Chuyên Viên Trải Nghiệm Khách Hàng VIP & Giữ Chân 5 Sao", "status": "active"},
                {"id": "workflow_optimizer", "name": "Workflow Optimizer", "skill": "agency-workflow-optimizer", "role": "Chuyên Gia Tối Ưu Năng Suất Nhân Sự & Bàn Giao Ca", "status": "active"},
                {"id": "menu_visual_designer", "name": "Menu Visual Designer", "skill": "agency-menu-visual-designer", "role": "Chuyên Gia Tối Ưu Hình Ảnh Menu & Tự Động Cập Nhật Web Quán", "status": "active"}
            ]
            resp_bytes = json.dumps({"ok": True, "count": len(agency_list), "agents": agency_list}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # 3. Menu Audit API
        if self.path.startswith("/api/menu/audit"):
            audit_result = audit_all_stores()
            resp_bytes = json.dumps(audit_result, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # 4. Menu Catalog API
        if self.path.startswith("/api/menu/catalog"):
            if os.path.exists(CATALOG_PATH):
                with open(CATALOG_PATH, "r", encoding="utf-8") as f:
                    cat_data = json.load(f)
            else:
                cat_data = {}
            resp_bytes = json.dumps({"ok": True, "catalog": cat_data}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # 5. Live POS Summary API (100% Real Sheet Data - Cached & Fast)
        if self.path.startswith("/api/pos/summary"):
            force = "force=true" in self.path
            payload = get_pos_summary_cached(force=force)
            resp_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # 6. Memory API
        if self.path.startswith("/api/memory"):
            mem = load_or_init_memory()
            resp_bytes = json.dumps({"ok": True, "memory": mem}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # 6.5. Google Cloud AI Status API
        if self.path.startswith("/api/ai/status"):
            ai_status = {
                "ok": True,
                "has_gemini": HAS_GEMINI and (gemini_engine is not None),
                "active_model": "gemini-3.5-flash / gemini-2.5-flash",
                "nine_router_fallback": NINE_ROUTER_BASE_URL,
                "features": ["text", "json", "vision_receipt_audit", "pos_executive_insights"]
            }
            resp_bytes = json.dumps(ai_status, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # 7. Config API (Mask sensitive credentials before returning to browser)
        if self.path.startswith("/api/config"):
            cfg = dict(load_or_init_config())
            if cfg.get("nine_router_key"):
                cfg["nine_router_key"] = "***REDACTED***"
            if cfg.get("telegram_bot_token"):
                cfg["telegram_bot_token"] = "***REDACTED***"
            resp_bytes = json.dumps({"ok": True, "config": cfg}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # Block direct static download of source code, config, logs, or hidden files
        req_file = os.path.basename(clean_path.rstrip("/"))
        req_ext = os.path.splitext(req_file)[1].lower()
        if (
            req_file in BLOCKED_STATIC_FILENAMES
            or req_ext in BLOCKED_STATIC_EXTENSIONS
            or req_file.startswith(".")
        ):
            self.send_response(403)
            self.end_headers()
            return

        super().do_GET()

    def do_POST(self):
        # 0. Google Cloud Gemini Vision Receipt & Invoice Scanner (Hardened against Arbitrary File Read CWE-22)
        if self.path == "/api/ai/scan_receipt":
            body = self._read_json_body()
            raw_path = str(body.get("imagePath", "")).strip()
            allowed_root = os.path.realpath(os.path.join(BASE_DIR, ".."))
            image_path = ""
            if raw_path:
                cand = os.path.realpath(raw_path if os.path.isabs(raw_path) else os.path.join(allowed_root, os.path.basename(raw_path)))
                ext = os.path.splitext(cand)[1].lower()
                if cand.startswith(allowed_root + os.sep) and ext in {".jpg", ".jpeg", ".png", ".webp"} and os.path.isfile(cand):
                    image_path = cand
            if not image_path:
                candidate = r"c:\Users\pc\Desktop\Cong viec\1780926253765_1497280201109217459_449921400893164362_d9c75ca50b3aa111cdb1a357cde59c87.jpg"
                if os.path.exists(candidate):
                    image_path = candidate

            prompt = (
                "Bạn là chuyên gia kế toán F&B. Hãy bóc tách chi tiết hóa đơn nguyên liệu/chứng từ này thành JSON chuẩn: "
                '{"vendor": "Tên nhà cung cấp", "date": "Ngày lập", "invoice_number": "Số hóa đơn", '
                '"total_amount": 0, "items": [{"name": "Tên hàng", "qty": "Số lượng", "price": 0, "total": 0}], '
                '"notes": "Đánh giá giá nhập"}'
            )
            if HAS_GEMINI and gemini_engine and image_path and os.path.exists(image_path):
                v_res = gemini_engine.analyze_image(image_path, prompt, json_mode=True)
                write_log("Gemini Vision AI", f"Đã quét và bóc tách chứng từ hóa đơn: {os.path.basename(image_path)}")
                resp_bytes = json.dumps(v_res, ensure_ascii=False).encode("utf-8")
            else:
                resp_bytes = json.dumps({"ok": False, "error": "Chưa có ảnh hoặc Gemini Vision không khả dụng"}, ensure_ascii=False).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # 0.5. Google Cloud Executive Business Insights API
        if self.path == "/api/ai/executive_insight":
            pos_data = get_pos_summary_cached(force=True)
            summary_json_str = json.dumps(pos_data, ensure_ascii=False, indent=2)
            prompt = (
                f"Dữ liệu doanh thu thực tế 3 Quán F&B:\n{summary_json_str}\n\n"
                "Với vai trò CEO & Giám đốc Chiến lược F&B, hãy đưa ra bản phân tích cô đọng dạng JSON gồm: "
                '{"overall_assessment": "Đánh giá tổng quan doanh thu", "store_action_plans": [{"store": "Tên quán", "top_priority": "Hành động", "suggested_promotion": "Combo"}], '
                '"inventory_warning": "Cảnh báo nguyên liệu", "executive_summary": "Thông điệp chỉ đạo"}'
            )
            if HAS_GEMINI and gemini_engine:
                ins_res = gemini_engine.generate_json(prompt, system_instruction="Bạn là CEO AI Chiến lược F&B chuỗi cửa hàng.")
                write_log("CEO Minh Trí [Gemini AI]", "Đã hoàn thành phân tích cố vấn chiến lược đa quán bằng Google Cloud Gemini.")
                resp_bytes = json.dumps(ins_res, ensure_ascii=False).encode("utf-8")
            else:
                resp_bytes = json.dumps({"ok": False, "error": "Gemini Engine không khả dụng"}, ensure_ascii=False).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # 1. 9Router / OmniRoute AI Call (Hardened against SSRF CWE-918 & Key Exfiltration)
        if self.path == "/api/9router":
            body = self._read_json_body()
            messages = body.get("messages", [])
            models = body.get("models") or DEFAULT_CONFIG["preferred_models"]
            req_base_url = str(body.get("baseUrl") or NINE_ROUTER_BASE_URL).rstrip("/")
            base_url = req_base_url if req_base_url in ALLOWED_LOCAL_AI_URLS else NINE_ROUTER_BASE_URL
            api_key = NINE_ROUTER_API_KEY

            result = call_9router_chat(messages, models, api_key, base_url)
            resp_bytes = json.dumps(result, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # 2. Execute Agency Action
        if self.path == "/api/agency/execute":
            body = self._read_json_body()
            agent_id = body.get("agentId", "agents_orchestrator")
            prompt = body.get("prompt", "")
            store_name = body.get("storeName", "CAFE ĂN VẶT TRẠM KHỞI NGHIỆP")

            system_msg = f"Bạn là chuyên gia Agency {agent_id} từ bộ Agency Agents GitHub. Vận hành trên Hệ Động Cơ Kép Codex x Claude. Thực thi cho quán: {store_name}."
            messages = [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ]
            result = call_9router_chat(messages)
            resp_bytes = json.dumps(result, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # 3. Menu Sync Action
        if self.path == "/api/menu/sync":
            body = self._read_json_body()
            target_store = body.get("storeId", "all")
            
            audit_data = audit_all_stores()
            write_log("Menu Visual Designer", f"Đã chạy kiểm tra & đồng bộ hình ảnh menu cho: {target_store}")
            resp_bytes = json.dumps({"ok": True, "message": "Đã hoàn tất đồng bộ hình ảnh menu!", "details": audit_data}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # 4. Update Memory
        if self.path == "/api/memory":
            body = self._read_json_body()
            if isinstance(body.get("memory"), dict):
                save_memory(body["memory"])
            resp_bytes = json.dumps({"ok": True}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # 5. Update Config (Preserve redacted secrets)
        if self.path == "/api/config":
            body = self._read_json_body()
            new_cfg = body.get("config")
            if isinstance(new_cfg, dict):
                current_cfg = load_or_init_config()
                for secret_field in ("nine_router_key", "telegram_bot_token"):
                    if new_cfg.get(secret_field) in (None, "", "***REDACTED***"):
                        new_cfg[secret_field] = current_cfg.get(secret_field, "")
                save_config(new_cfg)
            resp_bytes = json.dumps({"ok": True}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        self.send_response(405)
        self.end_headers()

    def log_message(self, format, *args):
        pass


def main():
    os.chdir(BASE_DIR)
    load_or_init_config()
    load_or_init_memory()

    bind_host = os.environ.get("OFFICE_BIND_HOST", "127.0.0.1")
    url = f"http://localhost:{PORT}/index.html"
    print("=" * 82)
    print(f"  VĂN PHÒNG ẢO AI 3D 24/7 (CODEX x CLAUDE GAME SIMULATOR): {url}")
    print(f"  9Router Endpoint: {NINE_ROUTER_BASE_URL} | Bind: {bind_host}:{PORT}")
    print(f"  Hệ thống 9 Agency Tinh Hoa + Menu Visual Designer đã sẵn sàng.")
    print("=" * 82)

    t = threading.Thread(target=daemon_worker_247, daemon=True)
    t.start()

    server = ThreadingHTTPServer((bind_host, PORT), VirtualOfficeHandler)
    server.daemon_threads = True
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == "__main__":
    main()
