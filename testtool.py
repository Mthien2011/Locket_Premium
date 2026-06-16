"""
Locket Friend Spam Tool - Python 3 (Đã sửa lỗi xử lý response - hỗ trợ result.data.uid)
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
FRIEND_REQUEST_ENDPOINT = "/sendFriendRequest"

USER_AGENTS = [
    "com.locket.Locket/2.51.0 iPhone/26.3.1 hw/iPhone12_3",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36"
]

class LocketSpamTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "*/*",
            "Accept-Language": "vi-VN,vi;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Host": "api.locketcamera.com"
        })
        self.token = None
        self.target_user_id = None
        self.target_username = None

    # ============================================
    # HÀM LẤY TOKEN
    # ============================================
    def get_auth_token(self):
        return "eyJhbGciOiJSUzI1NiIsImtpZCI6ImVlOTA0NmVhZDJlMDUwMDAxMGVkNTA0M2I0ODNkODRiMGM1MmM3YzQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQm8gRGVwWmFpIiwicmV2ZW51ZUNhdEVudGl0bGVtZW50cyI6W10sImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9sb2NrZXQtNDI1MmEiLCJhdWQiOiJsb2NrZXQtNDI1MmEiLCJhdXRoX3RpbWUiOjE3ODE2MjM5MjYsInVzZXJfaWQiOiJwVEcxSEhvck5ZZVFlUVFmaEV4dnBwNVJ1MDMzIiwic3ViIjoicFRHMUhIb3JOWWVRZVFRZmhFeHZwcDVSdTAzMyIsImlhdCI6MTc4MTYyMzkyNiwiZXhwIjoxNzgxNjI3NTI2LCJlbWFpbCI6Im1pbmh0aGllbjIyMDYyMDExQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJtaW5odGhpZW4yMjA2MjAxMUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.m6DB3oDLeLnYGCHmaPmLGxnhEkLCFk1VGOVGsrZim7LW9pwyGMj9wJBVOnxb_qrCE8A5Vb-nqClA94d8fqEjl67csDgvdJp5tIPG_V2xhl3jgDTxiUGdIBqz71UNvcgRw6Bllp9npexTwZm4MIft-gA61p2jLeAPEfFol1NSR5v2knbbAX-29jS3BhW5KPbAXhT8qKcg-s6t5XBN5GMv86ME0ndkd8PNNLm4OoGvnBAmWLQAR8Mrgq47UIjX7eYvrrfYL8L1bdhmYog98HlqsQFKABHs5T-l9gU0qIAxMN5-LZltQemD0Ycqr6iRhvii0JNEtWnnaEno8RghvKIimQ"

    # ============================================
    # HÀM LẤY HEADER BỔ SUNG
    # ============================================
    def get_extra_headers(self):
        return {
            "X-Firebase-AppCheck": "eyJraWQiOiJrMnhhbUEiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxOjY0MTAyOTA3NjA4Mzppb3M6Y2M4ZWI0NjI5MGQ2OWIyMzRmYTYwNiIsImF1ZCI6WyJwcm9qZWN0cy82NDEwMjkwNzYwODMiLCJwcm9qZWN0cy9sb2NrZXQtNDI1MmEiXSwicHJvdmlkZXIiOiJkZXZpY2VfY2hlY2tfZGV2aWNlX2lkZW50aWZpY2F0aW9uIiwiaXNzIjoiaHR0cHM6Ly9maXJlYmFzZWFwcGNoZWNrLmdvb2dsZWFwaXMuY29tLzY0MTAyOTA3NjA4MyIsImV4cCI6MTc4MTYyNjQwMSwiaWF0IjoxNzgxNjIyODAxLCJqdGkiOiJWa2xNcEtzTEVfOTg1TXdDdURXaXJLT1VpVkFqRjhSUnZyLWlqNjRwbkdrIn0.anGuigJuQNMR7DtoMxsBYpwTGShMVshmatCdoVdP-cJX3UwkOV7oPCtk_M6WKfgpPEuSSUP-jhg0V40bTtii-4FDScQOYqNpTu3mS6ZbpsG9khtfuyEEruo-343_KdXeT9ktA0fS4W1RFtrRiLtLZKxpmwxagr9erytLrZjP7vwovLHIX4KrAX8paGBP6Eqq8R8fWmJkguIXRsUsdRpUmeNKEr82dvmMxI_yD1NjFg2xsGko3YhUTRoAF9Vocioi2YzhvQgbrIqjQfHxS3Wi9XBS7Kf0RIa1LIjFhsr2UTM2i3KydAgh0oJNEeSr85eBckbHdBtLXntATy2gA0w9QDxOGnS1ssRVaveQv_-PuaKC68lmM831AUdnX949d3l-jlno5HB2zn5YmvEr5HvB0H0nxuevWxOWl0BbQs7lD9-Rt4yjWl02NyuDYs_VXyw4j9q3jgKrIxqjjsJ5dZHqrBzcu3Xmmtl3CeiXA1fIJDDYw6vgjxupl3p7NOgsoxao",
            "Firebase-Instance-ID-Token": "dhbFbJNPE00FuTSWpo2A2r:APA91bEBNvK4VnsPuMCuUSVxEBtoVEdWeEiTkT047UN4h_U4J05NrCy1xfUo-EFswrUjlkXe-GqQaXCCb0HbYHCADVaPe1fMTkSdLmySpcb7lZMYdgURJ3U",
            "sentry-trace": "422e4f55baa34d80afe36a180b978ea9-4d313a70ef4a40e7-0",
            "baggage": "sentry-environment=production,sentry-public_key=78fa64317f434fd89d9cc728dd168f50,sentry-release=com.locket.Locket%402.51.0%2B1,sentry-trace_id=422e4f55baa34d80afe36a180b978ea9"
        }

    # ============================================
    # HÀM TÌM KIẾM USERNAME - ĐÃ SỬA XỬ LÝ RESPONSE
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
        
        headers = self.session.headers.copy()
        headers["Authorization"] = f"Bearer {self.get_auth_token()}"
        
        extra_headers = self.get_extra_headers()
        for key, value in extra_headers.items():
            headers[key] = value
        
        # Thử cả hai dạng payload
        payloads = [
            {"username": username_or_link},
            {"data": {"username": username_or_link}}
        ]
        
        for payload in payloads:
            try:
                response = self.session.post(search_url, json=payload, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # ==== XỬ LÝ RESPONSE LINH HOẠT - ĐÃ SỬA ====
                    user = None
                    
                    # Trường hợp 1: response có dạng {"result": {"data": {"uid": "...", "first_name": "..."}}}
                    if data.get("result") and data["result"].get("data") and data["result"]["data"].get("uid"):
                        user_data = data["result"]["data"]
                        self.target_user_id = user_data.get("uid")
                        first_name = user_data.get("first_name", "")
                        last_name = user_data.get("last_name", "")
                        self.target_username = f"{first_name} {last_name}".strip()
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    # Trường hợp 2: response có dạng {"user": {"id": "...", "username": "..."}}
                    elif data.get("user"):
                        user = data["user"]
                        self.target_user_id = user.get("id")
                        self.target_username = user.get("username") or user.get("name") or "unknown"
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    # Trường hợp 3: response có dạng {"data": {"user": {"id": "...", "username": "..."}}}
                    elif data.get("data") and data["data"].get("user"):
                        user = data["data"]["user"]
                        self.target_user_id = user.get("id")
                        self.target_username = user.get("username") or user.get("name") or "unknown"
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    # Trường hợp 4: response có dạng {"users": [{"id": "...", "username": "..."}]}
                    elif data.get("users") and len(data["users"]) > 0:
                        user = data["users"][0]
                        self.target_user_id = user.get("id")
                        self.target_username = user.get("username") or user.get("name") or "unknown"
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    # Trường hợp 5: response trả về thẳng object user
                    elif data.get("id"):
                        self.target_user_id = data.get("id")
                        self.target_username = data.get("username") or data.get("name") or "unknown"
                        print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                        return True
                    
                    # Trường hợp 6: response có dạng {"data": {"id": "...", "username": "..."}}
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
        
        headers = self.session.headers.copy()
        headers["Authorization"] = f"Bearer {self.get_auth_token()}"
        
        extra_headers = self.get_extra_headers()
        for key, value in extra_headers.items():
            headers[key] = value
        
        payloads = [
            {"recipient_id": user_id, "source": "search"},
            {"userId": user_id, "source": "search"},
            {"friendId": user_id, "source": "search"},
            {"recipientId": user_id, "source": "search"},
            {"to": user_id, "source": "search"},
            {"data": {"recipient_id": user_id, "source": "search"}},
            {"data": {"userId": user_id, "source": "search"}}
        ]
        
        for payload in payloads:
            try:
                response = self.session.post(endpoint, json=payload, headers=headers, timeout=10)
                
                if response.status_code == 404:
                    endpoint2 = f"{BASE_URL}/v1/friends/requests"
                    response = self.session.post(endpoint2, json=payload, headers=headers, timeout=10)
                    if response.status_code in [200, 201, 204]:
                        return True, "Thành công"
                    continue
                
                if response.status_code in [200, 201, 204]:
                    return True, "Thành công"
                elif response.status_code == 429:
                    return False, "Bị giới hạn (rate limit)"
                elif response.status_code == 403:
                    return False, "Bị chặn hoặc token hết hạn"
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
        
        print(f"\n[+] Kết thúc: {success_count} thành công, {fail_count} thất bại")

    # ============================================
    # HÀM CHÍNH
    # ============================================
    def run(self):
        print("=" * 50)
        print("  LOCKET FRIEND SPAM TOOL v3.2")
        print("  (Đã sửa xử lý response - hỗ trợ result.data.uid)")
        print("=" * 50)
        
        while True:
            username_input = input("\n[?] Nhập Username hoặc Link kết bạn của Locket: ").strip()
            if username_input:
                if self.search_username(username_input):
                    break
                else:
                    print("[!] Vui lòng nhập lại.")
            else:
                print("[!] Không được bỏ trống.")
        
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