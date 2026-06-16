"""
Locket Friend Spam Tool - Python 3 (Bản hoàn chỉnh - đã tổng hợp toàn bộ header và endpoint)
"""

import requests
import json
import time
import random
import re
from urllib.parse import urlparse

# ============================================
# CẤU HÌNH - ĐÃ CẬP NHẬT THEO REQUEST THỰC TẾ
# ============================================
BASE_URL = "https://api.locketcamera.com"
SEARCH_ENDPOINT = "/getUserByUsername"
FRIEND_REQUEST_ENDPOINT = "/sendFriendRequest"

# ============================================
# HEADER CỐ ĐỊNH - LẤY TỪ REQUEST THỰC TẾ
# ============================================
USER_AGENT = "com.locket.Locket/2.51.0 iPhone/26.3.1 hw/iPhone12_3"
ACCEPT_LANGUAGE = "vi-VN,vi;q=0.9"
ACCEPT_ENCODING = "gzip, deflate, br"
CONNECTION = "keep-alive"
HOST = "api.locketcamera.com"
CONTENT_TYPE = "application/json"

# ============================================
# TOKEN - CẬP NHẬT TỪ STREAM MỖI KHI HẾT HẠN
# ============================================
AUTH_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImVlOTA0NmVhZDJlMDUwMDAxMGVkNTA0M2I0ODNkODRiMGM1MmM3YzQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQm8gRGVwWmFpIiwicmV2ZW51ZUNhdEVudGl0bGVtZW50cyI6W10sImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9sb2NrZXQtNDI1MmEiLCJhdWQiOiJsb2NrZXQtNDI1MmEiLCJhdXRoX3RpbWUiOjE3ODE2Mjc4MDcsInVzZXJfaWQiOiJwVEcxSEhvck5ZZVFlUVFmaEV4dnBwNVJ1MDMzIiwic3ViIjoicFRHMUhIb3JOWWVRZVFRZmhFeHZwcDVSdTAzMyIsImlhdCI6MTc4MTYyNzgwNywiZXhwIjoxNzgxNjMxNDA3LCJlbWFpbCI6Im1pbmh0aGllbjIyMDYyMDExQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJtaW5odGhpZW4yMjA2MjAxMUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.rYDHOSMDz-sTqGhynkWQXbFa0j80o-t0Z3NhCjCCD2udBgHue8TzH7gbCPdDA_Ldx_cTIz6XeY1DCgbf2zEtMT5lebwFUCZLTpHH7-6g4WRDR0Ah6EjXLz7-DQSmKuDGUHqr9FM7R_W_CVvKr6b0MK1t028gpluCK7GuYSH6AGTgT8c1yIelj2CkSKEoO-JgfP697lKII2F-BzTM9kGFuVq5u6HmA8_gLc-6bvI8KZExmNYV9idwBpzE9N2Qm9ppTmTte9ZcZEmaEz2RJj89cTew7qz15tdxSSrt1aRqQugUZCu7qMhFqy4Fto3MZt0XvkP3bQamJg6xLAKqUbVAKg"

FIREBASE_APP_CHECK = "eyJraWQiOiJrMnhhbUEiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxOjY0MTAyOTA3NjA4Mzppb3M6Y2M4ZWI0NjI5MGQ2OWIyMzRmYTYwNiIsImF1ZCI6WyJwcm9qZWN0cy82NDEwMjkwNzYwODMiLCJwcm9qZWN0cy9sb2NrZXQtNDI1MmEiXSwicHJvdmlkZXIiOiJkZXZpY2VfY2hlY2tfZGV2aWNlX2lkZW50aWZpY2F0aW9uIiwiaXNzIjoiaHR0cHM6Ly9maXJlYmFzZWFwcGNoZWNrLmdvb2dsZWFwaXMuY29tLzY0MTAyOTA3NjA4MyIsImV4cCI6MTc4MTYzMTIyMiwiaWF0IjoxNzgxNjI3NjIyLCJqdGkiOiJFVmpYYlpYREducEtiV3l0UTQycEVQZlRYVlhfV1ZNN1hvUlpPTkpyeWswIn0.xxRXvWsoZHrXdaQ-fl1CxpmdtcQ5qSncw5CwTd8azeAoE8A7kMC3dTzpmNa5Drvf9BR0k-0Igf4cb6OpuCcVc9-2kVcR05PCFp_OlIcJi8OcEDDP6R8qk-D7zRz8YbklZ7-ah1XiWoTEzg7r9Zhla-wNCekCO0mrbOWYfXJjb53X50_c0a9zVxb5S1A6h3g-yeW8RIwG8YLUywjG0tVpyEI3gq_8l0hEPkL1bwo2S5WKmGLDpAoKghuekzNv5dEL2ZmhQezDFjz4aHSYzGqHYnFauga_50rLvNA2mRflnCEuNZ0PONPWPzQ233cgrzPEwXjBDBIMV21Lv2gaM5XVHNV9Ne4CP_8IWmicXNYgI6Xrqn7ZUkrgzgpi4sFI5jI-0BfI_IEHCxh9uPzMPsM-bfEYN4iceYYJi1ekeJUKLYPObjNvZ63istvFaa9IES2McDzmJOPCG5r68uIcm9vvj4RmHRCwWSCCaYeamW2XRtRitM-sWLO4U2NyR0ZfKzwq"

FIREBASE_INSTANCE_ID = "dhbFbJNPE00FuTSWpo2A2r:APA91bEBNvK4VnsPuMCuUSVxEBtoVEdWeEiTkT047UN4h_U4J05NrCy1xfUo-EFswrUjlkXe-GqQaXCCb0HbYHCADVaPe1fMTkSdLmySpcb7lZMYdgURJ3U"

SENTRY_TRACE = "c1b7d248afb3419b970a54d41a3235fc-387e7ce90a5d4f3e-0"
BAGGAGE = "sentry-environment=production,sentry-public_key=78fa64317f434fd89d9cc728dd168f50,sentry-release=com.locket.Locket%402.51.0%2B1,sentry-trace_id=c1b7d248afb3419b970a54d41a3235fc"

# ============================================
# CLASS CHÍNH
# ============================================
class LocketSpamTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Host": HOST,
            "Accept": "*/*",
            "Accept-Language": ACCEPT_LANGUAGE,
            "Accept-Encoding": ACCEPT_ENCODING,
            "Content-Type": CONTENT_TYPE,
            "Connection": CONNECTION,
            "User-Agent": USER_AGENT,
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "X-Firebase-AppCheck": FIREBASE_APP_CHECK,
            "Firebase-Instance-ID-Token": FIREBASE_INSTANCE_ID,
            "sentry-trace": SENTRY_TRACE,
            "baggage": BAGGAGE
        })
        self.target_user_id = None
        self.target_username = None

    # ============================================
    # HÀM TÌM KIẾM USERNAME
    # ============================================
    def search_username(self, username_or_link):
        """
        Tìm kiếm tài khoản Locket theo username hoặc link
        """
        # Xử lý nếu là link
        if "locketcamera.com" in username_or_link or "locket" in username_or_link:
            parsed = urlparse(username_or_link)
            path_parts = parsed.path.split('/')
            username_or_link = path_parts[-1] if path_parts[-1] else path_parts[-2]
        
        print(f"\n[+] Đang tìm kiếm: {username_or_link}")
        
        search_url = f"{BASE_URL}{SEARCH_ENDPOINT}"
        
        # Thử cả hai dạng payload
        payloads = [
            {"username": username_or_link},
            {"data": {"username": username_or_link}}
        ]
        
        for payload in payloads:
            try:
                response = self.session.post(search_url, json=payload, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Xử lý response theo cấu trúc thực tế
                    user = None
                    
                    # Dạng 1: {"result": {"data": {"uid": "...", "first_name": "..."}}}
                    if data.get("result") and data["result"].get("data") and data["result"]["data"].get("uid"):
                        user_data = data["result"]["data"]
                        self.target_user_id = user_data.get("uid")
                        first_name = user_data.get("first_name", "")
                        last_name = user_data.get("last_name", "")
                        self.target_username = f"{first_name} {last_name}".strip()
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    # Dạng 2: {"user": {"id": "...", "username": "..."}}
                    elif data.get("user"):
                        user = data["user"]
                        self.target_user_id = user.get("id")
                        self.target_username = user.get("username") or user.get("name") or "unknown"
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    # Dạng 3: {"data": {"user": {"id": "...", "username": "..."}}}
                    elif data.get("data") and data["data"].get("user"):
                        user = data["data"]["user"]
                        self.target_user_id = user.get("id")
                        self.target_username = user.get("username") or user.get("name") or "unknown"
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    # Dạng 4: {"users": [{"id": "...", "username": "..."}]}
                    elif data.get("users") and len(data["users"]) > 0:
                        user = data["users"][0]
                        self.target_user_id = user.get("id")
                        self.target_username = user.get("username") or user.get("name") or "unknown"
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    # Dạng 5: trả về thẳng object user
                    elif data.get("id"):
                        self.target_user_id = data.get("id")
                        self.target_username = data.get("username") or data.get("name") or "unknown"
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    # Dạng 6: {"data": {"id": "...", "username": "..."}}
                    elif data.get("data") and data["data"].get("id"):
                        user = data["data"]
                        self.target_user_id = user.get("id")
                        self.target_username = user.get("username") or user.get("name") or "unknown"
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    else:
                        print(f"[-] Không tìm thấy user. Response: {json.dumps(data, indent=2)[:300]}")
                        return False
                
                elif response.status_code == 400:
                    # Thử payload tiếp theo
                    continue
                else:
                    print(f"[-] Lỗi API: {response.status_code} - {response.text[:200]}")
                    return False
                    
            except Exception as e:
                print(f"[-] Lỗi kết nối: {e}")
                continue
        
        return False

    # ============================================
    # HÀM GỬI LỜI MỜI KẾT BẠN
    # ============================================
    def send_friend_request(self, user_id):
        """
        Gửi 1 lời mời kết bạn đến user_id
        """
        endpoint = f"{BASE_URL}{FRIEND_REQUEST_ENDPOINT}"
        
        # Thử nhiều định dạng payload khác nhau
        payloads = [
            {"recipient_id": user_id, "source": "search"},
            {"userId": user_id, "source": "search"},
            {"friendId": user_id, "source": "search"},
            {"recipientId": user_id, "source": "search"},
            {"to": user_id, "source": "search"},
            {"data": {"recipient_id": user_id, "source": "search"}},
            {"data": {"userId": user_id, "source": "search"}},
            {"data": {"friendId": user_id, "source": "search"}}
        ]
        
        for payload in payloads:
            try:
                response = self.session.post(endpoint, json=payload, timeout=10)
                
                # Nếu 404, thử endpoint dự phòng
                if response.status_code == 404:
                    endpoint2 = f"{BASE_URL}/v1/friends/requests"
                    response = self.session.post(endpoint2, json=payload, timeout=10)
                    if response.status_code in [200, 201, 204]:
                        return True, "Thành công"
                    continue
                
                if response.status_code in [200, 201, 204]:
                    return True, "Thành công"
                elif response.status_code == 429:
                    return False, "Bị giới hạn (rate limit)"
                elif response.status_code == 403:
                    return False, "Bị chặn hoặc token hết hạn"
                elif response.status_code == 401:
                    return False, "Token hết hạn - cần lấy token mới"
                elif response.status_code == 400:
                    continue
                else:
                    return False, f"Lỗi {response.status_code}"
            except Exception as e:
                continue
        
        return False, "Không có payload nào hoạt động"

    # ============================================
    # HÀM SPAM LỜI MỜI
    # ============================================
    def spam_friend_requests(self, count):
        if not self.target_user_id:
            print("[-] Chưa có target. Hãy tìm kiếm trước.")
            return
        
        print(f"\n[+] Bắt đầu spam {count} lời mời đến {self.target_username} (ID: {self.target_user_id})")
        print("[+] Đang gửi...")
        
        success_count = 0
        fail_count = 0
        
        for i in range(1, count + 1):
            delay = random.uniform(0.5, 1.5)
            time.sleep(delay)
            
            success, message = self.send_friend_request(self.target_user_id)
            
            if success:
                success_count += 1
                print(f"  [{i}/{count}] ✓ Gửi thành công")
            else:
                fail_count += 1
                print(f"  [{i}/{count}] ✗ Thất bại: {message}")
            
            if "rate limit" in message.lower():
                print("[!] Phát hiện rate limit, tăng delay lên 8 giây...")
                time.sleep(8)
            
            if "token hết hạn" in message.lower():
                print("[!] Token đã hết hạn. Vui lòng lấy token mới từ Stream và cập nhật vào file.")
                break
        
        print(f"\n[+] Kết thúc: {success_count} thành công, {fail_count} thất bại")

    # ============================================
    # HÀM CHÍNH
    # ============================================
    def run(self):
        print("=" * 55)
        print("  LOCKET FRIEND SPAM TOOL v4.0")
        print("  (Bản hoàn chỉnh - tổng hợp header thực tế)")
        print("=" * 55)
        
        # Bước 1: Nhập username hoặc link
        while True:
            username_input = input("\n[?] Nhập Username hoặc Link kết bạn của Locket: ").strip()
            if username_input:
                if self.search_username(username_input):
                    break
                else:
                    print("[!] Vui lòng nhập lại.")
            else:
                print("[!] Không được bỏ trống.")
        
        # Bước 2: Nhập số lượng
        while True:
            try:
                count_input = input("[?] Nhập số lượng lời mời (1-100): ").strip()
                count = int(count_input)
                if 1 <= count <= 100:
                    break
                else:
                    print("[!] Vui lòng nhập số từ 1 đến 100.")
            except ValueError:
                print("[!] Vui lòng nhập số hợp lệ.")
        
        # Bước 3: Xác nhận và spam
        print(f"\n[+] Target: {self.target_username} (ID: {self.target_user_id})")
        print(f"[+] Số lượng: {count}")
        confirm = input("[?] Bắt đầu spam? (y/n): ").strip().lower()
        
        if confirm == 'y':
            self.spam_friend_requests(count)
        else:
            print("[+] Đã hủy.")

# ============================================
# ĐIỂM VÀO CHƯƠNG TRÌNH
# ============================================
if __name__ == "__main__":
    tool = LocketSpamTool()
    try:
        tool.run()
    except KeyboardInterrupt:
        print("\n[!] Đã dừng bởi người dùng.")
    except Exception as e:
        print(f"[-] Lỗi không mong muốn: {e}")