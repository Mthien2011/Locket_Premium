"""
Locket Friend Spam Tool - Python 3 (Bản fix lỗi 502 + tối ưu)
"""

import requests
import json
import time
import random
import re
from urllib.parse import urlparse

# ============================================
# CẤU HÌNH
# ============================================
BASE_URL = "https://api.locketcamera.com"
SEARCH_ENDPOINT = "/getUserByUsername"
FRIEND_REQUEST_ENDPOINT = "/v1/friends/requests"  # Đổi sang endpoint dự phòng để tránh 502

# ============================================
# HEADER CỐ ĐỊNH
# ============================================
USER_AGENT = "com.locket.Locket/2.51.0 iPhone/26.3.1 hw/iPhone12_3"
ACCEPT_LANGUAGE = "vi-VN,vi;q=0.9"
ACCEPT_ENCODING = "gzip, deflate, br"
CONNECTION = "keep-alive"
HOST = "api.locketcamera.com"
CONTENT_TYPE = "application/json"

# ============================================
# TOKEN - CẬP NHẬT TỪ STREAM
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
        self.retry_count = 0

    # ============================================
    # HÀM TÌM KIẾM USERNAME
    # ============================================
    def search_username(self, username_or_link):
        if "locketcamera.com" in username_or_link or "locket" in username_or_link:
            parsed = urlparse(username_or_link)
            path_parts = parsed.path.split('/')
            username_or_link = path_parts[-1] if path_parts[-1] else path_parts[-2]
        
        print(f"\n[+] Đang tìm kiếm: {username_or_link}")
        
        search_url = f"{BASE_URL}{SEARCH_ENDPOINT}"
        
        payloads = [
            {"username": username_or_link},
            {"data": {"username": username_or_link}}
        ]
        
        for payload in payloads:
            try:
                response = self.session.post(search_url, json=payload, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("result") and data["result"].get("data") and data["result"]["data"].get("uid"):
                        user_data = data["result"]["data"]
                        self.target_user_id = user_data.get("uid")
                        first_name = user_data.get("first_name", "")
                        last_name = user_data.get("last_name", "")
                        self.target_username = f"{first_name} {last_name}".strip()
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    elif data.get("user"):
                        user = data["user"]
                        self.target_user_id = user.get("id")
                        self.target_username = user.get("username") or user.get("name") or "unknown"
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    elif data.get("data") and data["data"].get("user"):
                        user = data["data"]["user"]
                        self.target_user_id = user.get("id")
                        self.target_username = user.get("username") or user.get("name") or "unknown"
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    elif data.get("users") and len(data["users"]) > 0:
                        user = data["users"][0]
                        self.target_user_id = user.get("id")
                        self.target_username = user.get("username") or user.get("name") or "unknown"
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    elif data.get("id"):
                        self.target_user_id = data.get("id")
                        self.target_username = data.get("username") or data.get("name") or "unknown"
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
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
                    continue
                else:
                    print(f"[-] Lỗi API: {response.status_code} - {response.text[:200]}")
                    return False
                    
            except Exception as e:
                print(f"[-] Lỗi kết nối: {e}")
                continue
        
        return False

    # ============================================
    # HÀM GỬI LỜI MỜI - ĐÃ FIX 502
    # ============================================
    def send_friend_request(self, user_id):
        """
        Gửi lời mời kết bạn - đa dạng endpoint và payload
        """
        # Danh sách endpoint sẽ thử
        endpoints = [
            f"{BASE_URL}/v1/friends/requests",
            f"{BASE_URL}/sendFriendRequest",
            f"{BASE_URL}/friends/add",
            f"{BASE_URL}/friend-request"
        ]
        
        # Danh sách payload sẽ thử
        payloads = [
            {"recipient_id": user_id},
            {"userId": user_id},
            {"friendId": user_id},
            {"recipientId": user_id},
            {"to": user_id},
            {"user_id": user_id},
            {"data": {"recipient_id": user_id}},
            {"data": {"userId": user_id}},
            {"data": {"friendId": user_id}}
        ]
        
        # Thêm source vào một số payload
        payloads_with_source = []
        for p in payloads[:5]:
            p_copy = p.copy()
            p_copy["source"] = "search"
            payloads_with_source.append(p_copy)
        payloads.extend(payloads_with_source)
        
        # Thử từng tổ hợp endpoint + payload
        for endpoint in endpoints:
            for payload in payloads:
                try:
                    # Reset session một chút để tránh bị cache
                    self.session.headers.update({
                        "Content-Length": str(len(json.dumps(payload)))
                    })
                    
                    response = self.session.post(endpoint, json=payload, timeout=15)
                    
                    # Xử lý response
                    if response.status_code in [200, 201, 204]:
                        return True, "Thành công"
                    
                    elif response.status_code == 502:
                        # Thử lại với delay dài hơn
                        time.sleep(3)
                        continue
                    
                    elif response.status_code == 429:
                        return False, "Rate limit"
                    
                    elif response.status_code == 403:
                        return False, "Bị chặn"
                    
                    elif response.status_code == 401:
                        return False, "Token hết hạn"
                    
                    elif response.status_code == 400:
                        continue
                    
                    else:
                        # Ghi log lỗi để debug
                        print(f"[DEBUG] Endpoint {endpoint} -> {response.status_code}")
                        continue
                        
                except requests.exceptions.Timeout:
                    continue
                except Exception as e:
                    continue
        
        return False, "Không có tổ hợp nào hoạt động"

    # ============================================
    # HÀM SPAM - VỚI CƠ CHẾ RETRY
    # ============================================
    def spam_friend_requests(self, count):
        if not self.target_user_id:
            print("[-] Chưa có target. Hãy tìm kiếm trước.")
            return
        
        print(f"\n[+] Bắt đầu spam {count} lời mời đến {self.target_username} (ID: {self.target_user_id})")
        print("[+] Đang gửi... (có thể mất vài phút)")
        
        success_count = 0
        fail_count = 0
        rate_limit_count = 0
        
        for i in range(1, count + 1):
            # Delay ngẫu nhiên, tăng dần nếu bị lỗi
            base_delay = random.uniform(1.5, 3.5)
            if self.retry_count > 3:
                base_delay += 5
            
            time.sleep(base_delay)
            
            success, message = self.send_friend_request(self.target_user_id)
            
            if success:
                success_count += 1
                self.retry_count = 0
                print(f"  [{i}/{count}] ✓ Gửi thành công")
            else:
                fail_count += 1
                self.retry_count += 1
                print(f"  [{i}/{count}] ✗ Thất bại: {message}")
            
            # Xử lý rate limit
            if "rate limit" in message.lower():
                rate_limit_count += 1
                wait_time = min(10 + rate_limit_count * 2, 30)
                print(f"[!] Rate limit, đợi {wait_time} giây...")
                time.sleep(wait_time)
            
            # Nếu token hết hạn, dừng
            if "token hết hạn" in message.lower():
                print("[!] Token đã hết hạn. Cập nhật token mới và chạy lại.")
                break
            
            # Nếu bị 502 liên tục, chờ lâu hơn
            if "502" in message and self.retry_count > 5:
                print("[!] Phát hiện lỗi 502 liên tục, đợi 60 giây...")
                time.sleep(60)
                self.retry_count = 0
        
        print(f"\n[+] Kết thúc: {success_count} thành công, {fail_count} thất bại")
        if rate_limit_count > 0:
            print(f"[!] Đã bị rate limit {rate_limit_count} lần")

    # ============================================
    # HÀM CHÍNH
    # ============================================
    def run(self):
        print("=" * 55)
        print("  LOCKET FRIEND SPAM TOOL v4.1")
        print("  (Đã fix lỗi 502 - thử nhiều endpoint)")
        print("=" * 55)
        
        while True:
            username_input = input("\n[?] Nhập Username hoặc Link kết bạn: ").strip()
            if username_input:
                if self.search_username(username_input):
                    break
                else:
                    print("[!] Vui lòng nhập lại.")
            else:
                print("[!] Không được bỏ trống.")
        
        while True:
            try:
                count_input = input("[?] Nhập số lượng lời mời (1-50): ").strip()
                count = int(count_input)
                if 1 <= count <= 50:
                    break
                else:
                    print("[!] Vui lòng nhập số từ 1 đến 50.")
            except ValueError:
                print("[!] Vui lòng nhập số hợp lệ.")
        
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