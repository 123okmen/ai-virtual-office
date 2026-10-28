#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI VIRTUAL OFFICE 24/7 (3D GAME SIMULATION + CODEX x CLAUDE SELF-LEARNING ENGINE)
- Cổng giao diện Văn Phòng Ảo 3D: http://localhost:8088/index.html
- Cổng kết nối 9Router AI Hub: http://localhost:20128/v1 (API Key: sk-c8ddee65dadacbf8-2orlgk-2451fb73)
- Động cơ kép: CODEX (cx/codex-auto-review, cx/gpt-5.6-sol) x CLAUDE (kr/claude-sonnet-4.5, kr/claude-haiku-4.5)
- Tách bạch 100% doanh thu, sổ kế toán và bộ nhớ tự học cho 2 quán:
  1. FOOD STATION 7A (Số 2, Đường 7A, KP. Phước Thiện, P. Long Bình, TP. Thủ Đức)
  2. TRẠM KHỞI NGHIỆP – Cơm Tấm Sườn Nướng Than Hoa & Cơm Chiên
  3. CAFE ĂN VẶT TRẠM KHỞI NGHIỆP (36/5E Nguyễn Thị Ngâu, Đông Thạnh, TP.HCM)
"""

import os
import sys
import json
import time
import threading
import webbrowser
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import urllib.request
import urllib.error

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

NINE_ROUTER_BASE_URL = "http://localhost:20128/v1"
NINE_ROUTER_API_KEY = "sk-c8ddee65dadacbf8-2orlgk-2451fb73"
GAS_URL_COMTAM = "https://script.google.com/macros/s/AKfycby8rz7upff345Kvv_pK-AVdClBsUit68aUgj4Cl8bvPN6vmM8_i8NZpJe2VqxE6Mc4qZQ/exec"

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
    "gas_url_7a": "",
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
            "agent": "Tuyết Mai - Kế Toán POS (Codex)",
            "engine": "cx/codex-auto-review",
            "insight": "Tỷ lệ giá vốn nguyên liệu chuẩn của FOOD STATION 7A cần giữ ở mức 34%-37%. Luôn gợi ý khách thêm Trứng/Phô mai (+5K) và Pepsi/Trà đá (+10K) để tăng biên lợi nhuận."
        },
        {
            "id": "mem_7a_3",
            "time": "Khởi tạo Hệ Thống",
            "agent": "Bảo Ngọc - Marketing (Claude)",
            "engine": "kr/claude-sonnet-4.5",
            "insight": "Khung 10h00 và 16h15 là giờ vàng đăng bài vào các hội nhóm cư dân Phước Thiện - Long Bình cho món Cơm Gà Xối Mỡ (40K), Mì Xào Giòn (40K) và Mì Cay 7 Cấp Độ (40K)."
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
            "agent": "Tuyết Mai - Kế Toán POS (Codex)",
            "engine": "cx/codex-auto-review",
            "insight": "Suất Cơm Tấm 2 Sườn (55K) cho Gymer và các topping Chả Trứng (+10K), Lạp Xưởng (+10K), Sườn Thêm (+25K) giúp tăng giá trị trung bình đơn (AOV) thêm 28%."
        },
        {
            "id": "mem_ct_3",
            "time": "Khởi tạo Hệ Thống",
            "agent": "Linh Nhi - CSKH (Claude)",
            "engine": "kr/claude-haiku-4.5",
            "insight": "Khi khách công ty đặt từ 5 hộp Cơm Tấm hoặc Cơm Chiên Dưa Bò (45K) trở lên, luôn xác nhận giờ giao trước 10h45 và gửi kèm link web đặt món nhanh."
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


def load_or_init_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not data.get("nine_router_key"):
                data["nine_router_key"] = NINE_ROUTER_API_KEY
                data["nine_router_url"] = NINE_ROUTER_BASE_URL
            return data
    except Exception:
        return DEFAULT_CONFIG


def load_or_init_memory() -> dict:
    if not os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_MEMORY, f, ensure_ascii=False, indent=2)
        return DEFAULT_MEMORY
    try:
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_MEMORY


def save_memory(mem_data: dict):
    try:
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(mem_data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def parse_9router_raw_response(raw_text: str) -> str:
    raw_text = (raw_text or "").strip()
    if not raw_text:
        return ""
    # Hỗ trợ cả JSON chuẩn và SSE stream (data: {...})
    if raw_text.startswith("data:"):
        chunks = []
        for line in raw_text.splitlines():
            line = line.strip()
            if line.startswith("data:") and line != "data: [DONE]":
                try:
                    obj = json.loads(line[5:].strip())
                    delta = obj.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    if not delta:
                        delta = obj.get("choices", [{}])[0].get("message", {}).get("content", "")
                    if delta:
                        chunks.append(delta)
                except Exception:
                    pass
        return "".join(chunks).strip()
    try:
        res_data = json.loads(raw_text)
        content = res_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if isinstance(content, list):
            content = "\n".join(
                part.get("text", "") if isinstance(part, dict) else str(part)
                for part in content
            )
        return (content or "").strip()
    except Exception:
        return ""


def call_9router_chat(messages: list, model_chain=None, api_key=NINE_ROUTER_API_KEY, base_url=NINE_ROUTER_BASE_URL):
    if not model_chain:
        model_chain = DEFAULT_CONFIG["preferred_models"]
    last_err = None
    for model_id in model_chain:
        try:
            payload = json.dumps({
                "model": model_id,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2200
            }).encode("utf-8")
            req = urllib.request.Request(
                f"{base_url.rstrip('/')}/chat/completions",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }
            )
            with urllib.request.urlopen(req, timeout=22) as resp:
                raw_text = resp.read().decode("utf-8", errors="ignore")
                content = parse_9router_raw_response(raw_text)
                if content:
                    return {"ok": True, "model": model_id, "content": content}
        except Exception as e:
            last_err = str(e)
            continue
    return {"ok": False, "error": last_err or "All models in chain failed"}


def fetch_live_pos_data(gas_url: str):
    if not gas_url:
        return None
    try:
        req = urllib.request.Request(gas_url + "?action=data", headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except Exception as e:
        write_log("POS Sync", f"Lỗi đọc Google Sheets API: {e}")
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
    write_log("Elite Agency Swarm", "Hệ thống 8 Agency Tinh Hoa (Github Suite) đã sẵn sàng phục vụ 3 Quán.")
    triggered_minutes = set()
    last_order_count = -1

    while True:
        try:
            cfg = load_or_init_config()
            now = datetime.now()
            hhmm = now.strftime("%H:%M")
            day_key = f"{now.strftime('%Y-%m-%d')}_{hhmm}"

            live = fetch_live_pos_data(cfg.get("gas_url_comtam", GAS_URL_COMTAM))
            if live and live.get("ok"):
                so_don = live.get("kpi", {}).get("soDon", 0)
                doanh_thu = live.get("kpi", {}).get("doanhThu", 0)
                if so_don != last_order_count:
                    last_order_count = so_don
                    write_log(
                        "NV4 Tuyết Mai [Codex POS]",
                        f"[SỔ 2 - {live.get('store')}] Ngày {live.get('ngay')}: {so_don} đơn | Doanh thu: {doanh_thu:,} đ"
                    )

            if hhmm in cfg.get("auto_schedule_times", []) and day_key not in triggered_minutes:
                triggered_minutes.add(day_key)
                rev_text = f"{live.get('kpi', {}).get('doanhThu', 0):,} đ" if live else "Đang cập nhật"
                msg = (
                    f"⏰ [CA TỰ ĐỘNG {hhmm}] Văn Phòng Ảo 3D 24/24 (Codex x Claude)\n"
                    f"🍔 Sổ 1: FOOD STATION 7A (Số 2 Đường 7A, Phước Thiện)\n"
                    f"🍛 Sổ 2: TRẠM KHỞI NGHIỆP Cơm Tấm (POS Live: {rev_text})\n"\
                    f"☕ Sổ 3: CAFE ĂN VẶT TRẠM KHỞI NGHIỆP (Đông Thạnh - Web App: http://localhost:8089/)"
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
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/api/agency"):
            agency_list = [
                {"id": "agents_orchestrator", "name": "Agents Orchestrator", "skill": "agency-agents-orchestrator", "status": "active"},
                {"id": "operations_manager", "name": "Operations Manager", "skill": "agency-operations-manager", "status": "active"},
                {"id": "pricing_analyst", "name": "Pricing Analyst", "skill": "agency-pricing-analyst", "status": "active"},
                {"id": "growth_hacker", "name": "Growth Hacker", "skill": "agency-growth-hacker", "status": "active"},
                {"id": "social_media_strategist", "name": "Social Media Strategist", "skill": "agency-social-media-strategist", "status": "active"},
                {"id": "analytics_reporter", "name": "Analytics Reporter", "skill": "agency-analytics-reporter", "status": "active"},
                {"id": "customer_service", "name": "Customer Service", "skill": "agency-customer-service", "status": "active"},
                {"id": "workflow_optimizer", "name": "Workflow Optimizer", "skill": "agency-workflow-optimizer", "status": "active"}
            ]
            resp_bytes = json.dumps({"ok": True, "count": len(agency_list), "agents": agency_list}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        if self.path.startswith("/api/memory"):
            mem = load_or_init_memory()
            resp_bytes = json.dumps({"ok": True, "memory": mem}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return
        super().do_GET()

    def do_POST(self):
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

        super().do_POST()

    def log_message(self, format, *args):
        pass


def main():
    os.chdir(BASE_DIR)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
    load_or_init_memory()

    url = f"http://localhost:{PORT}/index.html"
    print("=" * 82)
    print(f"  VĂN PHÒNG ẢO AI 3D 24/7 (CODEX x CLAUDE GAME SIMULATOR): {url}")
    print(f"  9Router Endpoint: {NINE_ROUTER_BASE_URL} | Key: {NINE_ROUTER_API_KEY}")
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
