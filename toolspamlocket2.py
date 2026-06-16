"""
Locket Friend Spam Tool - Python 3 (Đã sửa lỗi 404)
Cập nhật endpoint mới, hỗ trợ GET + POST
"""

import requests
import json
import time
import random
import re
from urllib.parse import urlparse

# ============================================
# CẤU HÌNH - CẬP NHẬT ENDPOINT MỚI
# ============================================
BASE_URL = "https://api.locketcamera.com"  # Domain giữ nguyên
SEARCH_ENDPOINT = "/users/search"           # Đã thử nghiệm với endpoint này
FRIEND_REQUEST_ENDPOINT = "/sendFriendRequest"  # Endpoint gửi lời mời

USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
]

class LocketSpamTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json"
        })
        self.token = None
        self.target_user_id = None
        self.target_username = None

    # ============================================
    # HÀM LẤY TOKEN - DÁN TOKEN VÀO ĐÂY
    # ============================================
    def get_auth_token(self):
        # THAY token giả này bằng token thật của bạn
        return "eyJhbGciOiJSUzI1NiIsImtpZCI6ImVlOTA0NmVhZDJlMDUwMDAxMGVkNTA0M2I0ODNkODRiMGM1MmM3YzQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQm8gRGVwWmFpIiwicmV2ZW51ZUNhdEVudGl0bGVtZW50cyI6W10sImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9sb2NrZXQtNDI1MmEiLCJhdWQiOiJsb2NrZXQtNDI1MmEiLCJhdXRoX3RpbWUiOjE3ODE2MjM5MjYsInVzZXJfaWQiOiJwVEcxSEhvck5ZZVFlUVFmaEV4dnBwNVJ1MDMzIiwic3ViIjoicFRHMUhIb3JOWWVRZVFRZmhFeHZwcDVSdTAzMyIsImlhdCI6MTc4MTYyMzkyNiwiZXhwIjoxNzgxNjI3NTI2LCJlbWFpbCI6Im1pbmh0aGllbjIyMDYyMDExQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJtaW5odGhpZW4yMjA2MjAxMUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.m6DB3oDLeLnYGCHmaPmLGxnhEkLCFk1VGOVGsrZim7LW9pwyGMj9wJBVOnxb_qrCE8A5Vb-nqClA94d8fqEjl67csDgvdJp5tIPG_V2xhl3jgDTxiUGdIBqz71UNvcgRw6Bllp9npexTwZm4MIft-gA61p2jLeAPEfFol1NSR5v2knbbAX-29jS3BhW5KPbAXhT8qKcg-s6t5XBN5GMv86ME0ndkd8PNNLm4OoGvnBAmWLQAR8Mrgq47UIjX7eYvrrfYL8L1bdhmYog98HlqsQFKABHs5T-l9gU0qIAxMN5-LZltQemD0Ycqr6iRhvii0JNEtWnnaEno8RghvKIimQ"

    # ============================================
    # HÀM TÌM KIẾM USERNAME - ĐÃ SỬA
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
        
        # ======== PHẦN SỬA ========
        # Thử endpoint /users/search với phương thức GET
        search_url = f"{BASE_URL}{SEARCH_ENDPOINT}"
        
        headers = self.session.headers.copy()
        headers["Authorization"] = f"Bearer {self.get_auth_token()}"
        
        # Tham số gửi dạng query string (GET)
        params = {
            "query": username_or_link,
            "limit": 10
        }
        
        try:
            # Dùng GET thay vì POST
            response = self.session.get(search_url, params=params, headers=headers, timeout=15)
            
            # Nếu GET bị lỗi 404, thử POST
            if response.status_code == 404:
                print("[!] GET không hoạt động, thử POST...")
                response = self.session.post(search_url, json=params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                # Kiểm tra cấu trúc response
                if data.get("users") and len(data["users"]) > 0:
                    user = data["users"][0]
                    self.target_user_id = user.get("id")
                    self.target_username = user.get("username") or user.get("name") or "unknown"
                    print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                    return True
                elif data.get("data") and data["data"].get("users"):
                    user = data["data"]["users"][0]
                    self.target_user_id = user.get("id")
                    self.target_username = user.get("username") or user.get("name") or "unknown"
                    print(f"[+] Tìm thấy: {self.target_username} (ID: {self.target_user_id})")
                    return True
                else:
                    print(f"[-] Không tìm thấy. Response: {json.dumps(data, indent=2)[:200]}")
                    return False
            else:
                print(f"[-] Lỗi API: {response.status_code} - {response.text[:200]}")
                return False
        except Exception as e:
            print(f"[-] Lỗi kết nối: {e}")
            return False

    # ============================================
    # HÀM GỬI LỜI MỜI KẾT BẠN - ĐÃ SỬA
    # ============================================
    def send_friend_request(self, user_id):
        """
        Gửi 1 lời mời kết bạn đến user_id
        """
        endpoint = f"{BASE_URL}{FRIEND_REQUEST_ENDPOINT}"
        
        headers = self.session.headers.copy()
        headers["Authorization"] = f"Bearer {self.get_auth_token()}"
        
        # Thử các payload khác nhau (tùy theo endpoint)
        payload = {
            "recipient_id": user_id,
            "source": "search"
        }
        
        try:
            response = self.session.post(endpoint, json=payload, headers=headers, timeout=10)
            
            # Nếu 404, thử endpoint /v1/friends/requests
            if response.status_code == 404:
                print("[!] /sendFriendRequest không tồn tại, thử /v1/friends/requests...")
                endpoint2 = f"{BASE_URL}/v1/friends/requests"
                response = self.session.post(endpoint2, json=payload, headers=headers, timeout=10)
            
            if response.status_code in [200, 201, 204]:
                return True, "Thành công"
            elif response.status_code == 429:
                return False, "Bị giới hạn (rate limit)"
            elif response.status_code == 403:
                return False, "Bị chặn hoặc token hết hạn"
            elif response.status_code == 400:
                return False, f"Bad Request - {response.text[:100]}"
            else:
                return False, f"Lỗi {response.status_code}"
        except Exception as e:
            return False, str(e)

    # ============================================
    # HÀM SPAM LỜI MỜI
    # ============================================
    def spam_friend_requests(self, count):
        """
        Spam lời mời kết bạn với số lượng count
        """
        if not self.target_user_id:
            print("[-] Chưa có target. Hãy tìm kiếm trước.")
            return
        
        print(f"\n[+] Bắt đầu spam {count} lời mời đến {self.target_username} (ID: {self.target_user_id})")
        print("[+] Đang gửi...")
        
        success_count = 0
        fail_count = 0
        
        for i in range(1, count + 1):
            # Thêm delay ngẫu nhiên để tránh phát hiện
            delay = random.uniform(0.5, 1.5)
            time.sleep(delay)
            
            success, message = self.send_friend_request(self.target_user_id)
            
            if success:
                success_count += 1
                print(f"  [{i}/{count}] ✓ Gửi thành công")
            else:
                fail_count += 1
                print(f"  [{i}/{count}] ✗ Thất bại: {message}")
            
            # Nếu bị rate limit, tăng delay
            if "rate limit" in message.lower():
                print("[!] Phát hiện rate limit, tăng delay lên 8 giây...")
                time.sleep(8)
        
        print(f"\n[+] Kết thúc: {success_count} thành công, {fail_count} thất bại")

    # ============================================
    # HÀM CHÍNH
    # ============================================
    def run(self):
        print("=" * 50)
        print("  LOCKET FRIEND SPAM TOOL v2.0")
        print("  (Đã sửa lỗi 404 - hỗ trợ GET/POST)")
        print("=" * 50)
        
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