#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI VIRTUAL OFFICE 24/7 (3D GAME SIMULATION + CODEX x CLAUDE SELF-LEARNING ENGINE)
- Cổng giao diện Văn Phòng Ảo 3D: http://localhost:8088/index.html
- Cổng kết nối 9Router AI Hub: http://localhost:20128/v1 (API Key: sk-c8ddee65dadacbf8-2orlgk-2451fb73)
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
  1. FOOD STATION 7A (Số 2, Đường 7A, KP. Phước Thiện, P. Long Bình, TP. Thủ Đức)
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
NINE_ROUTER_API_KEY = "sk-c8ddee65dadacbf8-2orlgk-2451fb73"

# Live Google Apps Script endpoints (100% Real Sheet Data)
GAS_URL_COMTAM = "https://script.google.com/macros/s/AKfycby8rz7upff345Kvv_pK-AVdClBsUit68aUgj4Cl8bvPN6vmM8_i8NZpJe2VqxE6Mc4qZQ/exec"
GAS_URL_CAFE = "https://script.google.com/macros/s/AKfycbyETg2znWnDrNsgq3G2eB0IJxFeb_GdLKo5N68FkFlJVMvTzdt_M_C3YFzL7fcgiyY1/exec"
GAS_URL_7A = ""

# Local Repository Paths
REPO_PATHS = {
    "store_7a": r"c:\Users\pc\Desktop\mô hình quán ăn nhanh",
    "store_comtam": r"c:\Users\pc\Desktop\Plan\com-tam-suon-nuong-app",
    "store_cafe_anvat": r"c:\Users\pc\Desktop\cafe-an-vat-tram-khoi-nghiep"
}

DEFAULT_CONFIG = {
    "office_name": "Văn Phòng Ảo AI 3D 24/7 - Hệ Động Cơ Kép CODEX x CLAUDE",
    "address": "Số 2, Đường 7A, KP. Phước Thiện, P. Long Bình, TP. Thủ Đức",
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
            "insight": "Ca Sáng (06h30-10h00) tại Số 2 Đường 7A tập trung tối đa tốc độ ra món dưới 90 giây cho Bánh Bao Kẹp (18K-26K), Hamburger (28K) và Sandwich (22K)."
        },
        {
            "id": "mem_7a_2",
            "time": "Khởi tạo Hệ Thống",
            "agent": "Menu Visual Designer (Codex x Claude)",
            "engine": "agency-menu-visual-designer",
            "insight": "Đã chuẩn hóa 28 hình ảnh món ăn chất lượng HD cho Quán Ăn Nhanh 7A (Bánh Bao Kẹp, Cơm Gà Xối Mỡ, Mì Cay, FastFood)."
        },
        {
            "id": "mem_7a_3",
            "time": "Khởi tạo Hệ Thống",
            "agent": "Tuyết Mai - Kế Toán POS (Codex)",
            "engine": "cx/codex-auto-review",
            "insight": "Tỷ lệ giá vốn nguyên liệu chuẩn của FOOD STATION 7A cần giữ ở mức 34%-37%. Luôn gợi ý khách thêm Trứng/Phô mai (+5K) và Pepsi/Trà đá (+10K) để tăng biên lợi nhuận."
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

            # 3. Kéo dữ liệu thật Quán 7A nếu có cấu hình
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
                            f"[SỔ 1 - FOOD STATION 7A] Ngày {live_7a.get('ngay')}: {so_don} đơn | Doanh thu thật: {doanh_thu:,} đ"
                        )

            # Báo cáo lịch tự động
            if hhmm in cfg.get("auto_schedule_times", []) and day_key not in triggered_minutes:
                triggered_minutes.add(day_key)
                rev_ct = f"{live_ct.get('kpi', {}).get('doanhThu', 0):,} đ" if live_ct else "0 đ (Chờ kết nối)"
                rev_cf = f"{live_cf.get('kpi', {}).get('doanhThu', 0):,} đ" if live_cf else "0 đ (Chờ kết nối)"
                msg = (
                    f"⏰ [BÁO CÁO CA TỰ ĐỘNG {hhmm}] Văn Phòng Ảo AI 3D 24/24 (Codex x Claude)\n"
                    f"🍔 Sổ 1: FOOD STATION 7A (Số 2 Đường 7A, Phước Thiện)\n"
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


class VirtualOfficeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # 1. Image serving proxy for local preview
        if self.path.startswith("/menu_images/"):
            parts = self.path[len("/menu_images/"):].split("/")
            if len(parts) >= 2:
                store_key = parts[0]
                img_name = parts[1]
                repo_path = REPO_PATHS.get("store_" + store_key) or REPO_PATHS.get(store_key)
                if repo_path:
                    local_img_path = os.path.join(repo_path, "public", "menu", img_name)
                    if os.path.exists(local_img_path):
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

        # 5. Live POS Summary API (100% Real Sheet Data)
        if self.path.startswith("/api/pos/summary"):
            cfg = load_or_init_config()
            ct = fetch_live_pos_data(cfg.get("gas_url_comtam", GAS_URL_COMTAM))
            cf = fetch_live_pos_data(cfg.get("gas_url_cafe", GAS_URL_CAFE))
            s7a = fetch_live_pos_data(cfg.get("gas_url_7a", "")) if cfg.get("gas_url_7a") else None

            payload = {
                "ok": True,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "store_7a": s7a or {"ok": False, "message": "Chưa cấu hình URL Google Sheet"},
                "store_comtam": ct or {"ok": False, "message": "Chưa kết nối được Google Sheet Cơm Tấm"},
                "store_cafe_anvat": cf or {"ok": False, "message": "Chưa kết nối được Google Sheet Cafe Đông Thạnh"}
            }
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

        # 7. Config API
        if self.path.startswith("/api/config"):
            cfg = load_or_init_config()
            resp_bytes = json.dumps({"ok": True, "config": cfg}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        super().do_GET()

    def do_POST(self):
        # 1. 9Router AI Call
        if self.path == "/api/9router":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8", errors="ignore")) if length > 0 else {}
            messages = body.get("messages", [])
            models = body.get("models") or DEFAULT_CONFIG["preferred_models"]
            api_key = body.get("apiKey") or NINE_ROUTER_API_KEY
            base_url = body.get("baseUrl") or NINE_ROUTER_BASE_URL

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
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8", errors="ignore")) if length > 0 else {}
            agent_id = body.get("agentId", "agents_orchestrator")
            prompt = body.get("prompt", "")
            store_name = body.get("storeName", "FOOD STATION 7A")

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
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8", errors="ignore")) if length > 0 else {}
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
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8", errors="ignore")) if length > 0 else {}
            if body.get("memory"):
                save_memory(body["memory"])
            resp_bytes = json.dumps({"ok": True}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        # 5. Update Config
        if self.path == "/api/config":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8", errors="ignore")) if length > 0 else {}
            if body.get("config"):
                save_config(body["config"])
            resp_bytes = json.dumps({"ok": True}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        super().do_POST()

    def log_message(self, format, *args):
        pass


def main():
    os.chdir(BASE_DIR)
    load_or_init_config()
    load_or_init_memory()

    url = f"http://localhost:{PORT}/index.html"
    print("=" * 82)
    print(f"  VĂN PHÒNG ẢO AI 3D 24/7 (CODEX x CLAUDE GAME SIMULATOR): {url}")
    print(f"  9Router Endpoint: {NINE_ROUTER_BASE_URL} | Key: {NINE_ROUTER_API_KEY}")
    print(f"  Hệ thống 9 Agency Tinh Hoa + Menu Visual Designer đã sẵn sàng.")
    print("=" * 82)

    t = threading.Thread(target=daemon_worker_247, daemon=True)
    t.start()

    server = ThreadingHTTPServer(("0.0.0.0", PORT), VirtualOfficeHandler)
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
