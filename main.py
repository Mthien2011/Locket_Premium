import threading 
import time 
import re 
import uuid 
import random 
import schedule 
import requests 
from datetime import datetime, timedelta 
from threading import Lock 
from bs4 import BeautifulSoup 
import tempfile 
import subprocess, sys 
import os 
import json 
from PIL import Image, ImageOps, ImageDraw, ImageFont 
from io import BytesIO 
from urllib.parse import urljoin, urlparse, urldefrag 
from telebot import TeleBot, types 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton 
from telegram.ext import Updater, CommandHandler, MessageHandler 
from time import strftime 
from concurrent.futures import ThreadPoolExecutor, as_completed 
from threading import Lock 
 
ALLOWED_GROUP_ID = -1003318308921 
allowed_group_id = -1003318308921 
last_spam_time = {} 
TOKEN = '8558431266:AAFN89-Q9xzG13zuq'   
bot = TeleBot(TOKEN) 
 
ADMIN_ID = 7782382498 
admins = {7782382498} 
QUAN_TRI_VIEN = [7782382498] 
user_keys = {} 
last_message_id = None 
allowed_users = set() 
blacklist = [] 
spam_processes = {} 
spam_users = {} 
user_spam_count = {} 
user_spam_time = {} 
user_callfree_count = {} 
user_callfree_time = {} 
full_spam_processes = {} 
lock = Lock() 
user_locks = {} 
last_command_time = {} 
 
bot_active = True 
start_time = time.time() 
 
@bot.message_handler(content_types=['new_chat_members']) 
def welcome_new_member(message): 
    for new_member in message.new_chat_members: 
        if new_member.id != bot.get_me().id: 
            welcome_message = bot.send_message(message.chat.id, f"👋 Wẻo Căm Bro {new_member.full_name} Đã Đến Nhóm Sì Pam Éc Em Éc, Nhập Lệnh /bot Để Hiển Thị Danh Sách Các Lệnh") 
            threading.Timer(1800, delete_welcome_message, args=(message.chat.id, welcome_message.message_id)).start() 
 
def delete_welcome_message(chat_id, message_id): 
    try: 
        bot.delete_message(chat_id, message_id) 
    except Exception as e: 
        print(f"Lỗi khi xóa tin nhắn: {str(e)}") 
 
def mask_sdt(sdt): 
    if len(sdt) == 10: 
        return f"{sdt[:3]}xxxx{sdt[-3:]}" 
    return sdt 
     
def get_network_provider(sdt): 
    network_providers = { 
        '086': 'Viettel', 
        '096': 'Viettel', 
        '097': 'Viettel', 
        '098': 'Viettel', 
        '032': 'Viettel', 
        '033': 'Viettel', 
        '034': 'Viettel', 
        '035': 'Viettel', 
        '036': 'Viettel', 
        '037': 'Viettel', 
        '038': 'Viettel', 
        '039': 'Viettel', 
        '091': 'VinaPhone', 
        '094': 'VinaPhone', 
        '088': 'VinaPhone', 
        '081': 'VinaPhone', 
        '082': 'VinaPhone', 
        '083': 'VinaPhone', 
        '084': 'VinaPhone', 
        '085': 'VinaPhone', 
        '089': 'MobiPhone', 
        '090': 'MobiPhone', 
        '093': 'MobiPhone', 
        '076': 'MobiPhone', 
        '077': 'MobiPhone', 
        '078': 'MobiPhone', 
        '079': 'MobiPhone', 
        '070': 'MobiPhone', 
        '058': 'Vietnamobile', 
        '052': 'Vietnamobile', 
        '056': 'Vietnamobile', 
        '092': 'Vietnamobile', 
    } 
    prefix = sdt[:3] 
    return network_providers.get(prefix, '"không xác định"') 
 
def load_keys(): 
    keys = { 
        'day': [], 
        'week': [], 
        'two_weeks': [], 
        'month': [] 
    } 
     
    try: 
        for duration in keys.keys(): 
            filename = f'keys_{duration}.txt' 
            if os.path.exists(filename): 
                with open(filename, 'r') as f: 
                    keys[duration] = [line.strip() for line in f.readlines()] 
    except Exception as e: 
        print(f"Lỗi: {e}") 
     
    return keys 
 
def save_keys(keys): 
    try: 
        for duration, key_list in keys.items(): 
            filename = f'keys_{duration}.txt' 
            with open(filename, 'w') as f: 
                for key in key_list: 
                    f.write(f"{key}\n") 
    except Exception as e: 
        print(f"Lỗi: {e}") 
 
def load_vip_users(): 
    if os.path.exists('vip_users.json'): 
        try: 
            with open('vip_users.json', 'r') as f: 
                data = json.load(f) 
                for user_id, status in data.items(): 
                    if status == "permanent": 
                        allowed_users.add(int(user_id)) 
                        user_keys[int(user_id)] = "permanent" 
                    else: 
                        user_keys[int(user_id)] = float(status) 
                        allowed_users.add(int(user_id)) 
        except json.JSONDecodeError: 
            print("Lỗi khi đọc tệp vip_users.json. Tệp có thể bị hỏng.") 
 
def save_vip_users(): 
    try: 
        vip_data = {user_id: user_keys[user_id] for user_id in allowed_users} 
        with open('vip_users.json', 'w') as f: 
            json.dump(vip_data, f) 
    except Exception as e: 
        print(f"Lỗi: {e}") 
 
def check_vip_status(user_id): 
    global allowed_users 
    # Đảm bảo allowed_users luôn là một set 
    if allowed_users is None: 
        allowed_users = set() 
 
    if user_id in user_keys: 
        current_time = time.time() 
        expiration_time = user_keys[user_id] 
        if expiration_time == "permanent": 
            return True 
        elif current_time > float(expiration_time): # Ép kiểu float để chắc chắn 
            allowed_users.discard(user_id) 
            if user_id in user_keys: 
                del user_keys[user_id] 
            save_vip_users() 
            return False 
        return True 
    return False     
 
def check_all_vip_status(): 
    while True: 
        for user_id in list(user_keys.keys()): 
            check_vip_status(user_id) 
        time.sleep(60) 
 
SUPER_VIP_FILE = 'super_vip.json' 
super_users = set() 
super_keys = {} 
 
def load_super_users(): 
    if os.path.exists(SUPER_VIP_FILE): 
        try: 
            with open(SUPER_VIP_FILE, 'r') as f: 
                data = json.load(f) 
                for user_id, status in data.items(): 
                    if status == "permanent": 
                        super_keys[int(user_id)] = "permanent" 
                    else: 
                        super_keys[int(user_id)] = float(status) 
                    super_users.add(int(user_id)) 
        except: 
            pass 
 
def save_super_users(): 
    try: 
        super_data = {user_id: super_keys[user_id] for user_id in super_users} 
        with open(SUPER_VIP_FILE, 'w') as f: 
            json.dump(super_data, f) 
    except Exception as e: 
        print(f"Lỗi lưu Super VIP: {e}") 
 
def check_super_status(user_id): 
    if user_id == ADMIN_ID: return True 
    if user_id in super_keys: 
        status = super_keys[user_id] 
        if status == "permanent": return True 
        if time.time() > float(status): 
            super_users.discard(user_id) 
            super_keys.pop(user_id, None) 
            save_super_users() 
            return False 
        return True 
    return False 
 
# Gọi load khi khởi động 
load_super_users() 
 
def get_remaining_days(expiration_time): 
    if expiration_time == "permanent": 
        return "Vĩnh Viễn" 
     
    remaining_time = expiration_time - time.time() 
    if remaining_time <= 0: 
        return "Đã hết hạn" 
     
    days = int(remaining_time // 86400) 
    hours = int((remaining_time % 86400) // 3600) 
     
    if days > 0: 
        return f"{days} ngày {hours} giờ" 
    else: 
        return f"{hours} giờ" 
 
def get_remaining_days_vip(status): 
    if status == "permanent": 
        return "VIP Vĩnh Viễn" 
     
    remaining_time = float(status) - time.time() 
    if remaining_time <= 0: 
        return "Đã hết hạn" 
     
    days = int(remaining_time // 86400) 
    hours = int((remaining_time % 86400) // 3600) 
     
    if days > 0: 
        return f"Hết hạn sau: {days} ngày {hours} giờ" 
    else: 
        return f"Hết hạn sau: {hours} giờ nữa" 
         
AUTO_DATA_FILE = 'auto_data.json' 
 
def load_auto_data(): 
    if os.path.exists(AUTO_DATA_FILE): 
        with open(AUTO_DATA_FILE, 'r') as f: return json.load(f) 
    return {} 
 
def save_auto_data(data): 
    with open(AUTO_DATA_FILE, 'w') as f: json.dump(data, f, indent=4) 
 
# Hàm chạy tự động lúc 00:00 và 06:00 
def run_auto_spam(): 
    data = load_auto_data() 
    if not data: 
        bot.send_message(ALLOWED_GROUP_ID, "🔔 <b>THÔNG BÁO HỆ THỐNG</b>\n<blockquote>Đã đến giờ chạy tự động nhưng danh sách hiện đang trống!</blockquote>", parse_mode="HTML") 
        return 
     
    # Thông báo bắt đầu có thêm thông tin số lần 
    bot.send_message(ALLOWED_GROUP_ID, f''' 
🔔 <b>BẮT ĐẦU CHẠY TỰ ĐỘNG</b> 
<blockquote>» Thời điểm: {time.strftime('%H:%M')} 
» Tổng số mục tiêu: {len(data)} SĐT 
» Số lần mặc định: 10 
» Trạng thái: Đang khởi tạo luồng...</blockquote> 
''', parse_mode="HTML") 
 
    for sdt in data.keys(): 
        # Thêm tham số '30' vào sau sdt 
        threading.Thread(target=lambda s=sdt: subprocess.run(['python', 'dec.py', s, '10'])).start() 
        # Nghỉ một chút giữa các luồng để tránh quá tải CPU 
        time.sleep(5)  
 
def schedule_checker(): 
    # Bạn có thể thêm nhiều khung giờ khác ở đây nếu muốn 
    schedule.every().day.at("00:00").do(run_auto_spam) 
    schedule.every().day.at("06:00").do(run_auto_spam) 
    while True: 
        schedule.run_pending() 
        time.sleep(1) 
 
# Chạy luồng kiểm tra thời gian ngầm 
threading.Thread(target=schedule_checker, daemon=True).start() 
 
REF_FILE = 'referrals.json' 
JOINED_USERS_FILE = 'joined_users.json' # Để chống cheat (người cũ vào lại không tính) 
 
def load_data(file, default_type=dict): 
    if os.path.exists(file): 
        with open(file, 'r') as f: return json.load(f) 
    return default_type() 
 
def save_data(file, data): 
    with open(file, 'w') as f: json.dump(data, f, indent=4) 
 
# Khởi tạo dữ liệu 
referrals = load_data(REF_FILE) 
joined_users = load_data(JOINED_USERS_FILE, list) 
 
def run_vip_background(user_id, valid_numbers): 
    if user_id not in vip_processes: 
        vip_processes[user_id] = [] 
     
    for sdt in valid_numbers: 
        try: 
            # Khởi chạy file dec.py cho từng số 
            p = subprocess.Popen(['python', 'dec.py', sdt, '10']) 
            vip_processes[user_id].append(p) 
            # Nghỉ 0.5s giữa mỗi số để tránh quá tải CPU đột ngột 
            time.sleep(5)  
        except Exception as e: 
            print(f"Lỗi khởi chạy số {sdt}: {e}") 
             
def check_process_status(sdt, process): 
    start_time = time.time() 
    while True: 
        if process.poll() is not None: 
            del spam_processes[sdt] 
            break 
        if time.time() - start_time > 300: 
            process.terminate() 
            del spam_processes[sdt] 
            break 
        time.sleep(10) 
 
SPAM_COUNT_FILE = 'spam_count.json' 
 
def load_spam_counts(): 
    global user_spam_count, user_spam_time 
    try: 
        with open(SPAM_COUNT_FILE, 'r') as f: 
            data = json.load(f) 
            user_spam_count = data.get('spam_count', {}) 
            user_spam_time = data.get('spam_time', {}) 
    except (FileNotFoundError, json.JSONDecodeError): 
        user_spam_count = {} 
        user_spam_time = {} 
 
def save_spam_counts(): 
    with open(SPAM_COUNT_FILE, 'w') as f: 
        json.dump({ 
            'spam_count': user_spam_count, 
            'spam_time': user_spam_time 
        }, f) 
 
def reset_spam_counts(): 
    while True: 
        now = datetime.now() 
        next_reset = (datetime.combine(now.date() + timedelta(days=1), datetime.min.time()) - now).total_seconds() 
        time.sleep(next_reset) 
        user_spam_count.clear() 
        user_spam_time.clear() 
        save_spam_counts() 
 
threading.Thread(target=reset_spam_counts, daemon=True).start() 
 
valid_keys = load_keys() 
allowed_users = load_vip_users() 
 
SPAM_COUNT_FILE = 'spam_count.json' 
 
@bot.message_handler(commands=['taokey']) 
def generate_key(message): 
    if message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ Bạn không có quyền sử dụng lệnh này!') 
        return 
 
    params = message.text.split()[1:] 
    if len(params) != 1: 
        bot.reply_to(message, '» Định dạng: <code>/taokey [số ngày]</code>', parse_mode="HTML") 
        return 
 
    try: 
        days = int(params[0]) 
        new_key = str(uuid.uuid4()) # Tạo key định dạng 2de5b146... 
         
        keys = load_keys() 
         
        # Tự động phân loại dựa trên số ngày để khớp với hàm load_keys() cũ 
        category = 'day' 
        if days >= 30: category = 'month' 
        elif days >= 14: category = 'two_weeks' 
        elif days >= 7: category = 'week' 
         
        if category not in keys: 
            keys[category] = [] 
             
        keys[category].append(new_key) 
        save_keys(keys) 
 
        response = f''' 
✅ <b>TẠO KEY THÀNH CÔNG</b> 
<blockquote><b>Thông Tin Key:</b> 
» Key: <code>{new_key}</code> 
» Thời hạn: {days} ngày 
» Loại: {category}</blockquote> 
<i>Gửi key này cho người dùng để kích hoạt!</i> 
''' 
        bot.reply_to(message, response, parse_mode="HTML") 
 
    except Exception as e: 
        bot.reply_to(message, f'❌ Lỗi:') 
         
@bot.message_handler(commands=['key']) 
def check_key(message): 
    if message.chat.id != ALLOWED_GROUP_ID: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong Nhóm Chỉ Định') 
        return 
     
    user_id = message.from_user.id 
    if not bot_active and user_id != ADMIN_ID: 
        bot.reply_to(message, '❌ BOT Đang OFF...') 
        return 
     
    # Kiểm tra VIP cũ 
    if user_id in allowed_users: 
        if check_vip_status(user_id): 
            bot.reply_to(message, '❌ VIP Của Bạn Vẫn Còn Hiệu Lực!') 
            return 
 
    params = message.text.split()[1:] 
    if len(params) != 1: 
        bot.reply_to(message, '» Định dạng: <code>/key [MÃ_KEY]</code>', parse_mode="HTML") 
        return 
 
    input_key = params[0].strip() 
    keys = load_keys() 
     
    key_found = False 
    seconds_to_add = 0 
    duration_text = "" 
 
    # Cấu trúc mapping để quét qua các mục trong file keys 
    mapping = { 
        'day': (86400, "24 Giờ"), 
        'week': (604800, "7 Ngày"), 
        'two_weeks': (1209600, "14 Ngày"), 
        'month': (2592000, "30 Ngày") 
    } 
 
    for category, info in mapping.items(): 
        if category in keys and input_key in keys[category]: 
            seconds_to_add = info[0] 
            duration_text = info[1] 
            keys[category].remove(input_key) 
            key_found = True 
            break 
 
    if key_found: 
        try: bot.delete_message(message.chat.id, message.message_id) 
        except: pass 
 
        expiration_time = time.time() + seconds_to_add 
        user_keys[user_id] = expiration_time 
        allowed_users.add(user_id) 
         
        save_keys(keys) 
        save_vip_users() 
         
        exp_date = time.strftime('%H:%M:%S — %d-%m-%Y', time.localtime(expiration_time)) 
         
        # Phản hồi bọc trong blockquote 
        response_msg = f''' 
✅ <b>KÍCH HOẠT THÀNH CÔNG!</b> 
<blockquote><b>Thông tin VIP:</b> 
» Gói: {duration_text} 
» Hết hạn: <code>{exp_date}</code> 
» Trạng thái: Đang hoạt động</blockquote> 
''' 
        bot.send_message(message.chat.id, response_msg, parse_mode="HTML") 
    else: 
        bot.reply_to(message, '❌ Key không tồn tại hoặc đã được sử dụng!') 
 
threading.Thread(target=check_all_vip_status, daemon=True).start() 
 
@bot.message_handler(commands=['id']) 
def send_user_id(message): 
    if message.chat.id != allowed_group_id and message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
 
    user_id = message.from_user.id 
    user_full_name = message.from_user.full_name 
    user_username = message.from_user.username 
    if message.reply_to_message: 
        replied_user_id = message.reply_to_message.from_user.id 
        replied_user_full_name = message.reply_to_message.from_user.full_name 
        replied_user_username = message.reply_to_message.from_user.username   
        bot.reply_to(message, f''' 
» User <blockquote>{replied_user_full_name}</blockquote>» ID <blockquote>{replied_user_id}</blockquote>» Username <blockquote>@{replied_user_username}</blockquote>''', parse_mode="HTML") 
    else: 
        bot.reply_to(message, f''' 
» User <blockquote>{user_full_name}</blockquote>» ID <blockquote>{user_id}</blockquote>» Username <blockquote>@{user_username}</blockquote>''', parse_mode="HTML") 
 
@bot.message_handler(commands=['addvip']) 
def add_vip(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
 
    if message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ Mày Đéo Có Quyền Sử Dụng Lệnh Này Đâu, Chỉ QuanghauDz Mới Có Quyền Ra Lệnh ADDVIP') 
        return 
 
    params = message.text.split()[1:] 
     
    if len(params) < 1: 
        bot.reply_to(message, "» Cú pháp: <code>/addvip [ID]</code> hoặc <code>/addvip [ID] [Số Ngày]</code>", parse_mode="HTML") 
        return 
 
    try: 
        user_id = int(params[0]) 
         
        # Kiểm tra nếu có nhập số ngày hay không 
        if len(params) >= 2: 
            days = int(params[1]) 
            # Tính toán thời gian hết hạn (Thời gian hiện tại + số ngày quy ra giây) 
            expiration_time = time.time() + (days * 86400) 
            user_keys[user_id] = expiration_time 
            han_su_dung = f"{days} Ngày" 
            exp_date = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(expiration_time)) 
            chi_tiet_han = f"Hết Hạn Lúc: {exp_date}" 
        else: 
            # Nếu không nhập số ngày, mặc định là vĩnh viễn 
            user_keys[user_id] = "permanent" 
            han_su_dung = "Vĩnh Viễn" 
            chi_tiet_han = "Hạn Sử Dụng: Không Giới Hạn" 
 
        allowed_users.add(user_id) 
        save_vip_users() 
         
        bot.reply_to(message, f''' 
✅ <b>ADD VIP THÀNH CÔNG</b> 
┌───⭓ 
<blockquote>» ID: <code>{user_id}</code> 
» Thời Hạn: {han_su_dung} 
» {chi_tiet_han}</blockquote> 
└───⧕ 
        ''', parse_mode="HTML") 
 
    except ValueError: 
        bot.reply_to(message, "❌ Sai định dạng! ID và Số ngày phải là con số.") 
 
@bot.message_handler(commands=['delvip']) 
def del_vip(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
 
    if message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ Mày Đéo Có Quyền Sử Dụng Lệnh Này Đâu, Chỉ QuanghauDz Mới Có Quyền Ra Lệnh DELVIP') 
        return 
 
    params = message.text.split()[1:] 
 
    user_id = int(params[0]) 
    if user_id in allowed_users: 
        allowed_users.discard(user_id) 
        user_keys.pop(user_id, None) 
        save_vip_users() 
        bot.reply_to(message, f'✅ ID {user_id} Đã Bị Xóa Khỏi Danh Sách VIP') 
    else: 
        bot.reply_to(message, f'❌ ID {user_id} Không Có Trong Danh Sách VIP') 
 
@bot.message_handler(commands=['addsuper']) 
def add_super(message): 
    if message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ Chỉ Admin mới có quyền cấp SUPER VIP!') 
        return 
 
    params = message.text.split()[1:] 
    if len(params) < 1: 
        bot.reply_to(message, "» Cú pháp: <code>/addsuper [ID]</code> hoặc <code>/addsuper [ID] [Số Ngày]</code>", parse_mode="HTML") 
        return 
 
    try: 
        user_id = int(params[0]) 
        if len(params) >= 2: 
            days = int(params[1]) 
            expiration_time = time.time() + (days * 86400) 
            super_keys[user_id] = expiration_time 
            han_text = f"{days} Ngày" 
            exp_date = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(expiration_time)) 
            detail = f"Hết Hạn: {exp_date}" 
        else: 
            super_keys[user_id] = "permanent" 
            han_text = "Vĩnh Viễn" 
            detail = "Hạn Dùng: Không Giới Hạn" 
 
        super_users.add(user_id) 
        save_super_users() 
         
        bot.reply_to(message, f''' 
✅ <b>ADD SUPER VIP THÀNH CÔNG</b> 
<blockquote>» ID: <code>{user_id}</code> 
» Thời Hạn: {han_text} 
» {detail}</blockquote>''', parse_mode="HTML") 
    except ValueError: 
        bot.reply_to(message, "❌ ID và Số ngày phải là con số.") 
 
@bot.message_handler(commands=['delsuper']) 
def del_super(message): 
    # Chỉ Admin hoặc Quản trị viên cấp cao mới có quyền xóa 
    if message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ Bạn không có quyền thực hiện lệnh này!') 
        return 
 
    params = message.text.split()[1:] 
    if len(params) < 1: 
        bot.reply_to(message, "» Cú pháp: <code>/delsuper [ID]</code>", parse_mode="HTML") 
        return 
 
    try: 
        user_id = int(params[0]) 
         
        if user_id in super_users: 
            super_users.discard(user_id) 
            super_keys.pop(user_id, None) 
            save_super_users() 
             
            bot.reply_to(message, f''' 
✅ <b>GỠ QUYỀN SUPER VIP THÀNH CÔNG</b> 
<blockquote>» ID: <code>{user_id}</code> 
» Trạng thái: Đã trở về tài khoản thường.</blockquote>''', parse_mode="HTML") 
        else: 
            bot.reply_to(message, f"❌ ID <code>{user_id}</code> không có trong danh sách SUPER VIP.", parse_mode="HTML") 
             
    except ValueError: 
        bot.reply_to(message, "❌ ID phải là con số.") 
         
 
@bot.message_handler(commands=['ping']) 
def ping(message): 
 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
    if bot_active == False and message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ BOT Đã Trong Trạng Thái OFF, Chỉ QuanghauDz Mới Được Sử Dụng BOT Lúc OFF, Vui Lòng Đợi BOT ON Để Tiếp Tục Sử Dụng') 
        return 
 
    start_date = datetime(2024, 11, 28) 
    current_time = datetime.now() 
    uptime = current_time - start_date 
 
    uptime_days = uptime.days 
 
    start_time_ping = time.time() 
    loading = bot.reply_to(message, "♻️ Đang Kiểm Tra BOT SMS...") 
    end_time_ping = time.time() 
    latency = (end_time_ping - start_time_ping) 
    bot.delete_message(chat_id=loading.chat.id, message_id=loading.message_id) 
    bot.reply_to(message, f''' 
✅ Đã Kiểm Tra Xong BOT SMS 
 
» BOT Trả Lời Trong 
<blockquote>{latency:.2f} Giây</blockquote> 
» BOT Đã Hoạt Động 
<blockquote>{uptime_days} Ngày</blockquote> 
''', parse_mode="HTML") 
 
@bot.message_handler(commands=['off']) 
def bot_off(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
    global bot_active 
    if message.from_user.id == ADMIN_ID: 
        bot_active = False 
        bot.reply_to(message, '✅ BOT Đã Trong Trạng Thái OFF') 
    else: 
        bot.reply_to(message, '❌ Mày Đéo Có Quyền Sử Dụng Lệnh Này Đâu, Chỉ QuanghauDz Mới Có Quyền Ra Lệnh OFF') 
 
@bot.message_handler(commands=['on']) 
def bot_on(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
    global bot_active 
    if message.from_user.id == ADMIN_ID: 
        bot_active = True 
        bot.reply_to(message, '✅ BOT Đã Trong Trạng Thái ON') 
    else: 
        bot.reply_to(message, '❌ Mày Đéo Có Quyền Sử Dụng Lệnh Này Đâu, Chỉ QuanghauDz Mới Có Quyền Ra Lệnh ON') 
 
MUTE_FILE = 'muted_users.json' 
 
def load_muted_users(): 
    if os.path.exists(MUTE_FILE): 
        with open(MUTE_FILE, 'r') as f: 
            return json.load(f) 
    return {} 
 
def save_muted_users(muted_users): 
    with open(MUTE_FILE, 'w') as f: 
        json.dump(muted_users, f) 
 
muted_users = load_muted_users() 
 
@bot.message_handler(commands=['mute']) 
def mute(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
 
    if message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ Mày Đéo Có Quyền Sử Dụng Lệnh Này Đâu, Chỉ QuanghauDz Mới Có Quyền Ra Lệnh MUTE') 
        return 
 
    params = message.text.split()[1:] 
 
    user_id = int(params[0]) 
    time_input = params[1] 
 
    time_match = re.match(r'(\d+)([mhd])', time_input) 
    if not time_match: 
        bot.reply_to(message, '❌ Thời Gian Không Hợp Lệ! Vui Lòng Nhập Đúng Định Dạng (vd: 1m, 1h, 1d)') 
        return 
 
    time_value = int(time_match.group(1)) 
    time_unit = time_match.group(2) 
 
    if time_unit == 'm': 
        mute_time = time_value * 60 
    elif time_unit == 'h': 
        mute_time = time_value * 3600 
    elif time_unit == 'd': 
        mute_time = time_value * 86400 
 
    try: 
        bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=False) 
        if time_unit == 'm': 
            bot.reply_to(message, f'✅ Một Thằng Ngu Đã Bị ĐạiKa Tao Bịt Mồm Trong {time_value} Phút') 
        elif time_unit == 'h': 
            bot.reply_to(message, f'✅ Một Thằng Ngu Đã Bị ĐạiKa Tao Bịt Mồm Trong {time_value} Giờ') 
        elif time_unit == 'h': 
            bot.reply_to(message, f'✅ Một Thằng Ngu Đã Bị ĐạiKa Tao Bịt Mồm Trong {time_value} Ngày') 
 
        muted_users[user_id] = { 
            'mute_time': mute_time, 
            'unmute_at': time.time() + mute_time 
        } 
        save_muted_users(muted_users) 
 
        threading.Timer(mute_time, unmute_user, args=(message.chat.id, user_id)).start() 
    except Exception as e: 
        bot.reply_to(message, f'❌ Lỗi: {str(e)}') 
 
def unmute_user(chat_id, user_id): 
    try: 
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True) 
        if user_id in muted_users: 
            del muted_users[user_id] 
            save_muted_users(muted_users) 
    except Exception as e: 
        bot.send_message(chat_id, f'❌ Lỗi Khi Mở Khóa Thành Viên ID {user_id}: {str(e)}') 
 
def check_muted_users_loop(): 
    while True: 
        current_time = time.time() 
        for user_id, info in list(muted_users.items()): 
            if current_time >= info['unmute_at']: 
                unmute_user(allowed_group_id, int(user_id)) 
        time.sleep(30) # Kiểm tra mỗi 30 giây 
 
@bot.message_handler(commands=['unmute']) 
def unmute(message): 
    # Kiểm tra nhóm hợp lệ 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
 
    # Kiểm tra quyền Admin 
    if message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ Chỉ QuanghauDz mới có quyền mở mõm cho người khác!') 
        return 
 
    params = message.text.split()[1:] 
    if len(params) < 1: 
        bot.reply_to(message, '❌ Vui lòng nhập ID người dùng cần unmute. (VD: /unmute 12345678)') 
        return 
 
    try: 
        user_id = int(params[0]) 
         
        # Mở khóa các quyền gửi tin nhắn, media, v.v. 
        bot.restrict_chat_member( 
            message.chat.id,  
            user_id,  
            can_send_messages=True,  
            can_send_media_messages=True,  
            can_send_polls=True,  
            can_send_other_messages=True,  
            can_add_web_page_previews=True 
        ) 
 
        # Xóa khỏi file lưu trữ muted_users 
        if user_id in muted_users: 
            del muted_users[user_id] 
            save_muted_users(muted_users) 
 
        bot.reply_to(message, f'✅ Đã mở mõm cho ID {user_id}. Lần sau bớt ngu lại nhé!') 
         
    except ValueError: 
        bot.reply_to(message, '❌ ID người dùng không hợp lệ!') 
    except Exception as e: 
        bot.reply_to(message, f'❌ Lỗi: {str(e)}') 
 
@bot.message_handler(commands=['ban']) 
def ban_user(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Lệnh này chỉ dùng được trong nhóm chỉ định!') 
        return 
 
    if message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ Bạn không có quyền sử dụng lệnh này!') 
        return 
 
    params = message.text.split()[1:] 
    if len(params) < 1: 
        bot.reply_to(message, '❌ Cú pháp: /ban [User_ID]') 
        return 
 
    try: 
        user_id = int(params[0]) 
        bot.ban_chat_member(message.chat.id, user_id) 
        bot.reply_to(message, f'✅ Đã cút! ID {user_id} đã bị ĐạiKa tiễn vong khỏi nhóm.') 
    except Exception as e: 
        bot.reply_to(message, f'❌ Lỗi: {str(e)}') 
 
@bot.message_handler(commands=['unban']) 
def unban_user(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Lệnh này chỉ dùng được trong nhóm chỉ định!') 
        return 
 
    if message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ Bạn không có quyền sử dụng lệnh này!') 
        return 
 
    params = message.text.split()[1:] 
    if len(params) < 1: 
        bot.reply_to(message, '❌ Cú pháp: /unban [User_ID]') 
        return 
 
    try: 
        user_id = int(params[0]) 
        # only_if_banned=True giúp tránh lỗi nếu user chưa bị ban 
        bot.unban_chat_member(message.chat.id, user_id, only_if_banned=True) 
        bot.reply_to(message, f'✅ Đã ân xá cho ID {user_id}. Bây giờ nó có thể vào lại nhóm.') 
    except Exception as e: 
        bot.reply_to(message, f'❌ Lỗi: {str(e)}') 
         
@bot.message_handler(commands=['bot']) 
def send_welcome(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
     
    if bot_active == False and message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ BOT Đã Trong Trạng Thái OFF, Chỉ QuanghauDz Mới Được Sử Dụng BOT Lúc OFF, Vui Lòng Đợi BOT ON Để Tiếp Tục Sử Dụng') 
        return 
 
    bot.reply_to(message, f''' 
┌───⭓ Spam SMS x CALL 
<blockquote>» Spam + Call 
» /spamvip : Spam sms vip 
» /spam : Spam sms free 
» /callvip : call vip 
» /full : spam call cộng sms 
» /stopfull : dừng spam call cộng sms 
» /aotu : thêm sdt vào danh sách aotu để hệ thống tự chạy 
» /listaotu : xem sdt mình đã thêm vào danh sách aotu 
» /xoaaotu : xoá số đã thêm aotu 
» /status : SĐT Đang Spam 
» /stop : Dừng Spam SĐT 
» /stopcallfree : dừng spam call free 
» /stopcallvip : dừng call vip 
» /key : Nhập Key Đã Mua 
» /muavip : Mua + Free VIP 
» /uservip : Danh Sách UserVip               
» /usersuper : Danh Sách UserSuper               
» /checkme : Check VIP 
» /warning : Lưu Ý Khi Spam</blockquote> 
└───⧕ 
 
┌───⭓ lệnh admin 
<blockquote>» /addvip : Cấp Vip Spam 
» /delvip : xoá quyền vip 
» /addsuper : cấp quyền super 
» /delsuper : xoá quyền super 
» /addblacklist : thêm số điện thoại cấm 
» /delblacklist : xoá số cấm 
» /mute : khoá mỗm 
» /unmute : mở mỗm 
» /ban : cút 
» /unban : hết cút</blockquote> 
└───⧕ 
 
┌───⭓ lệnh mời link giới thiệu 
<blockquote>» /share : Link Share đủ 5 người vip 1 ngày free</blockquote> 
└───⧕ 
 
┌───⭓ Contact 
<blockquote>» /admin : Liên Hệ ADMIN 
» Mua Vip Ủng Hộ Admin Tele @quanghau8th7</blockquote> 
└───⧕ 
    ''', parse_mode="HTML") 
 
@bot.message_handler(commands=['muavip']) 
def muavip(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
    if bot_active == False and message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ BOT Đã Trong Trạng Thái OFF, Chỉ QuanghauDz Mới Được Sử Dụng BOT Lúc OFF, Vui Lòng Đợi BOT ON Để Tiếp Tục Sử Dụng') 
        return 
    bot.reply_to(message, f''' 
┌───⭓ Mua Key Spam VIP 
<blockquote>» Liên Hệ Admin @quanghau8th7 
 
» Key Free, Key Tuần, Key Tháng Spam SMS Giá Rẻ</blockquote> 
└───⧕ 
    ''', parse_mode="HTML") 
 
@bot.message_handler(commands=['warning']) 
def warning(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
    if bot_active == False and message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ BOT Đã Trong Trạng Thái OFF, Chỉ QuanghauDz Mới Được Sử Dụng BOT Lúc OFF, Vui Lòng Đợi BOT ON Để Tiếp Tục Sử Dụng') 
        return 
    bot.reply_to(message, f''' 
<blockquote>» Lưu Ý: Hãy Sử Dụng Spam 1 Cách Thông Minh, Không Nên Spam 1 Số Quá Nhiều Lần Trong Khoảng Thời Gian Ngắn Sẽ Khiến Các Bên API Chặn Số Không Thể Get OTP, Bot Sẽ Không Chịu Trách Nhiệm Nếu Bạn Sử Dụng Spam Nhầm Mục Đích Vi Phạm Pháp Luật!!</blockquote> 
    ''', parse_mode="HTML") 
 
def vip(): 
    global last_message_id 
    while True: 
        try: 
            if last_message_id is not None: 
                try: 
                    bot.delete_message(allowed_group_id, last_message_id) 
                except: 
                    pass 
             
            sent_message = bot.send_message(allowed_group_id, ''' 
<blockquote>» Key Free, Key Tuần, Key Tháng Spam SMS Giá Rẻ 
» Liên Hệ Admin @quanghau8th7</blockquote> 
 
<blockquote>» Admin @quanghau8th7</blockquote> 
            ''', parse_mode="HTML") 
             
            last_message_id = sent_message.message_id 
        except Exception as e: 
            print(f"Lỗi gửi tin nhắn VIP: {e}") 
         
        time.sleep(120) # Gửi lại sau mỗi 2 tiếng 
 
    # Khởi chạy thread vip 
    threading.Thread(target=vip, daemon=True).start() 
 
@bot.message_handler(commands=['admin']) 
def diggory(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
    if bot_active == False and message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ BOT Đã Trong Trạng Thái OFF, Chỉ QuanghauDz Mới Được Sử Dụng BOT Lúc OFF, Vui Lòng Đợi BOT ON Để Tiếp Tục Sử Dụng') 
        return 
    diggory_chat = f''' 
<blockquote>» @quanghau8th7</blockquote> 
    ''' 
    bot.reply_to(message, diggory_chat, parse_mode="HTML") 
 
last_usage = {} 
 
@bot.message_handler(commands=['checkme']) 
def check(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
    if not bot_active and message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ BOT Đã Trong Trạng Thái OFF, Vui Lòng Đợi BOT ON Để Tiếp Tục Sử Dụng') 
        return 
 
    user_id = message.from_user.id 
    user_username = message.from_user.username if message.from_user.username else "Không có" 
    full_name = message.from_user.full_name 
 
    # 1. KIỂM TRA SUPER VIP TRƯỚC 
    if check_super_status(user_id): 
        status = super_keys.get(user_id) 
        if status == "permanent": 
            exp_msg = "Vĩnh Viễn" 
            countdown = "Vô thời hạn" 
        else: 
            exp_msg = time.strftime("%H:%M:%S, %d/%m/%Y", time.localtime(float(status))) 
            countdown = get_remaining_days(status) # Sử dụng hàm tính ngày đã viết ở trên 
 
        bot.reply_to(message, f''' 
┌───⭓ <b>THÔNG TIN TÀI KHOẢN</b> 
<blockquote>» Tên: <b>{message.from_user.full_name}</b> 
» ID: <code>{user_id}</code></blockquote> 
└───⧕ 
 
┌───⭓ <b>CẤP ĐỘ: SUPER VIP 👑</b> 
<blockquote>» Hạn dùng: {exp_msg} 
» Còn lại: {countdown}</blockquote> 
└───⧕''', parse_mode="HTML") 
 
    # 2. KIỂM TRA VIP THƯỜNG 
    elif user_id in allowed_users: 
        expiration_time = user_keys.get(user_id) 
        if expiration_time == "permanent": 
            exp_msg = "VIP Vĩnh Viễn" 
            countdown = "Vô thời hạn" 
        else: 
            exp_msg = time.strftime("%H:%M:%S, %d/%m/%Y", time.localtime(float(expiration_time))) 
            countdown = get_remaining_days(expiration_time) 
 
        bot.reply_to(message, f''' 
┌───⭓ <b>THÔNG TIN TÀI KHOẢN</b> 
<blockquote>» Tên: <b>{message.from_user.full_name}</b> 
» ID: <code>{user_id}</code></blockquote> 
└───⧕ 
 
┌───⭓ <b>CẤP ĐỘ: USER VIP 👤</b> 
<blockquote>» Hạn dùng: {exp_msg} 
» Còn lại: {countdown}</blockquote> 
└───⧕''', parse_mode="HTML") 
 
    # 3. TÀI KHOẢN FREE 
    else: 
        bot.reply_to(message, f''' 
┌───⭓ <b>THÔNG TIN TÀI KHOẢN</b> 
<blockquote>» Tên: <b>{message.from_user.full_name}</b> 
» ID: <code>{user_id}</code></blockquote> 
└───⧕ 
 
┌───⭓ <b>CẤP ĐỘ: USER FREE 🆓</b> 
<blockquote>» Trạng thái: Bình thường 
» Gia hạn: Liên hệ Admin hoặc dùng /share</blockquote> 
└───⧕''', parse_mode="HTML") 
 
@bot.message_handler(commands=['reset']) 
def restart_bot(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
    if message.from_user.id == ADMIN_ID: 
        loading = bot.reply_to(message, "♻️ Đang Khởi Động Lại BOT SMS... Vui Lòng Đợi 3 Giây") 
        time.sleep(3) 
        bot.delete_message(chat_id=loading.chat.id, message_id=loading.message_id) 
        bot.reply_to(message, "✅ BOT Đã Khởi Động Lại Thành Công!!")  
        os.execv(sys.executable, ['python'] + sys.argv)       
    else: 
        bot.reply_to(message, "❌ Mày Đéo Có Quyền Sử Dụng Lệnh Này Đâu, Chỉ QuanghauDz Mới Có Quyền Ra Lệnh Reset") 
 
@bot.message_handler(commands=['spam']) 
def spam(message): 
    # --- XÓA TIN NHẮN LỆNH CỦA NGƯỜI DÙNG --- 
    try: 
        bot.delete_message(message.chat.id, message.message_id) 
    except: 
        pass # Tránh lỗi nếu bot không có quyền xóa tin nhắn 
 
    if message.chat.id != allowed_group_id: 
        bot.send_message(message.chat.id, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
    if bot_active == False and message.from_user.id != ADMIN_ID: 
        bot.send_message(message.chat.id, '❌ BOT Đang OFF, Vui Lòng Đợi BOT ON Để Tiếp Tục Sử Dụng') 
        return 
         
    user_id = message.from_user.id 
    user_username = message.from_user.username 
 
    params = message.text.split()[1:] 
    if len(params) != 1: 
        msg = bot.send_message(message.chat.id, f''' 
» SAI ĐỊNH DẠNG!!! 
<blockquote>» /spam + SĐT 
» VD: /spam 0987654321</blockquote> 
        ''', parse_mode="HTML") 
        # Tự xóa thông báo lỗi sau 5 giây để tránh rác nhóm 
        threading.Timer(5, lambda: bot.delete_message(message.chat.id, msg.message_id)).start() 
        return 
 
    sdt = params[0] 
    if not sdt.isdigit() or len(sdt) != 10: 
        bot.send_message(message.chat.id, "❌ SĐT Không Hợp Lệ (Phải là 10 số)") 
        return 
 
    # Kiểm tra Blacklist 
    if sdt in blacklist: 
        bot.send_message(message.chat.id, f''' 
» Á À Tao Bắt Quả Tang Nhóc Spam Blacklist Nhé 
┌───⭓ 
<blockquote>» {message.from_user.full_name}</blockquote> 
└───⧕ 
        ''', parse_mode="HTML") 
        return 
 
    # Kiểm tra đang chạy 
    if sdt in spam_processes: 
        bot.send_message(message.chat.id, f"❌ SĐT [{mask_sdt(sdt)}] Đang Được Spam, Vui Lòng Đợi!") 
        return 
     
    current_time = time.time() 
     
    # Cooldown 30s 
    if user_id in last_usage and current_time - last_usage[user_id] < 120: 
        bot.send_message(message.chat.id, f"❌ Thích Spam Lắm Không? {120 - (current_time - last_usage[user_id]):.0f} Giây Nữa Nhé") 
        return 
     
    # Giới hạn 5 lần/ngày 
    if user_id not in user_spam_time or current_time - user_spam_time[user_id] > 86400: 
        user_spam_count[user_id] = 0 
        user_spam_time[user_id] = current_time 
 
    if user_spam_count.get(user_id, 0) >= 3: 
        bot.send_message(message.chat.id, '❌ Bạn Đã Dùng Hết 3/3 Lần FREE Hôm Nay. Mua VIP Để Ko Giới Hạn!') 
        return 
 
    # Lưu trạng thái 
    last_usage[user_id] = current_time 
    user_spam_count[user_id] = user_spam_count.get(user_id, 0) + 1 
    save_spam_counts() 
     
    network_provider = get_network_provider(sdt) 
    masked_phone = mask_sdt(sdt)  
     
    loading = bot.send_message(message.chat.id, '⏳') 
 
    def spam_task(): 
        script_filename = "dec.py" 
        if os.path.isfile(script_filename): 
            process = subprocess.Popen(["python", script_filename, sdt, "5"]) 
            spam_processes[sdt] = process 
            spam_users[sdt] = user_id  
             
            bot.delete_message(chat_id=loading.chat.id, message_id=loading.message_id) 
             
            response = f''' 
┌───⭓ 
<blockquote>» Name {message.from_user.full_name}</blockquote> 
└───⧕ 
┌───⭓ 
<blockquote>» Server: Spam SMS FREE 
» Target: [{masked_phone}] 
» Nhà Mạng: [{network_provider}] 
» Vòng Lặp: 5 
» Hôm Nay: {user_spam_count[user_id]}/5</blockquote> 
└───⧕ 
<b>Dừng Lệnh:</b> <code>/stop sdt</code> 
            ''' 
            bot.send_message(message.chat.id, response, parse_mode="HTML") 
            threading.Thread(target=check_process_status, args=(sdt, process)).start() 
        else: 
            bot.send_message(message.chat.id, "❌ Không tìm thấy file dec.py") 
 
    threading.Thread(target=spam_task).start() 
     
@bot.message_handler(commands=['spamvip']) 
def supersms(message): 
    # 1. XÓA TIN NHẮN LỆNH CỦA NGƯỜI DÙNG NGAY LẬP TỨC 
    try: 
        bot.delete_message(message.chat.id, message.message_id) 
    except: 
        pass 
 
    # 2. KIỂM TRA NHÓM VÀ TRẠNG THÁI BOT 
    if message.chat.id != allowed_group_id and message.from_user.id != ADMIN_ID: 
        bot.send_message(message.chat.id, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
    if bot_active == False and message.from_user.id != ADMIN_ID: 
        bot.send_message(message.chat.id, '❌ BOT Đang OFF, Vui Lòng Đợi BOT ON Để Tiếp Tục Sử Dụng') 
        return 
         
    user_id = message.from_user.id 
    user_username = message.from_user.username if message.from_user.username else "NoUsername" 
     
    # 3. KIỂM TRA QUYỀN VIP 
    if not check_vip_status(user_id) and user_id not in allowed_users: 
        msg = bot.send_message(message.chat.id, f''' 
» Bạn Là User FREE, Không Thể Sử Dụng /spamvip, Hãy Sử Dụng /spam Hoặc Mua VIP 
<blockquote>» /muavip : Mua VIP + Key Free</blockquote> 
        ''', parse_mode="HTML") 
        return 
 
    # 4. KIỂM TRA THAM SỐ SĐT 
    params = message.text.split()[1:] 
    if len(params) != 1: 
        msg = bot.send_message(message.chat.id, f''' 
» SAI ĐỊNH DẠNG!!! 
<blockquote>» /spamvip + SĐT 
» VD: /spamvip 0987654321</blockquote> 
        ''', parse_mode="HTML") 
        # Tự xóa thông báo lỗi sau 5s 
        threading.Timer(5, lambda: bot.delete_message(message.chat.id, msg.message_id)).start() 
        return 
 
    sdt = params[0] 
    if not sdt.isdigit() or len(sdt) != 10: 
        bot.send_message(message.chat.id, "❌ Vui lòng nhập đúng SĐT 10 số") 
        return 
 
    # 5. KIỂM TRA BLACKLIST VÀ TRẠNG THÁI ĐANG CHẠY 
    if sdt in blacklist: 
        bot.send_message(message.chat.id, f''' 
» Á À Tao Bắt Quả Tang Nhóc Spam Blacklist Nhé 
┌───⭓ 
<blockquote>» {message.from_user.full_name}</blockquote> 
└───⧕ 
        ''', parse_mode="HTML") 
        return 
 
    if sdt in spam_processes: 
        bot.send_message(message.chat.id, f"❌ SĐT [{mask_sdt(sdt)}] Đang Được Spam, Vui Lòng Đợi!") 
        return 
     
    # 6. KIỂM TRA COOLDOWN 30S 
    current_time = time.time() 
    if user_id in last_usage and current_time - last_usage[user_id] < 30: 
        bot.send_message(message.chat.id, f"❌ Chờ {30 - (current_time - last_usage[user_id]):.0f}s nữa để tiếp tục") 
        return 
     
    # LƯU TRẠNG THÁI 
    last_usage[user_id] = current_time 
    user_spam_count[user_id] = user_spam_count.get(user_id, 0) + 1 
    save_spam_counts() 
     
    # LẤY THÔNG TIN HIỂN THỊ (ẨN SỐ) 
    network_provider = get_network_provider(sdt) 
    masked_phone = mask_sdt(sdt) 
    formatted_time = time.strftime("%H:%M:%S, %d/%m/%Y") 
     
    loading = bot.send_message(message.chat.id, '⏳') 
 
    def spam_task(): 
        script_filename = "dec.py" 
        if os.path.isfile(script_filename): 
            count = 10 
            # CHẠY TIẾN TRÌNH TRỰC TIẾP (GIẢM THIỂU FILE TẠM ĐỂ TỐI ƯU RAM) 
            process = subprocess.Popen(["python", script_filename, sdt, str(count)]) 
             
            spam_processes[sdt] = process 
            spam_users[sdt] = user_id 
             
            bot.delete_message(chat_id=loading.chat.id, message_id=loading.message_id) 
             
            response = f''' 
┌───⭓ 
<blockquote>» Name {message.from_user.full_name}</blockquote> 
└───⧕ 
┌───⭓ 
<blockquote>» Server: Spam SMS VIP 
» Target: [{masked_phone}] 
» Nhà Mạng: [{network_provider}] 
» Vòng Lặp: {count} 
» Gói: [VIP] 
» Lúc: [{formatted_time}] 
» Dừng: [/stop sdt]</blockquote> 
└───⧕ 
    ''' 
            bot.send_message(message.chat.id, response, parse_mode="HTML") 
             
            # Luồng theo dõi để tự động xóa số khi chạy xong 
            threading.Thread(target=check_process_status, args=(sdt, process)).start() 
        else: 
            bot.send_message(message.chat.id, "❌ Tập tin dec.py không tồn tại.") 
 
    threading.Thread(target=spam_task).start() 
 
@bot.message_handler(commands=['callvip']) 
def callvip_cmd(message): 
    # 1. XÓA TIN NHẮN LỆNH CỦA NGƯỜI DÙNG 
    try: 
        bot.delete_message(message.chat.id, message.message_id) 
    except: 
        pass 
 
    # 2. KIỂM TRA QUYỀN HẠN NHÓM VÀ TRẠNG THÁI BOT 
    if message.chat.id != allowed_group_id and message.from_user.id != ADMIN_ID: 
        bot.send_message(message.chat.id, f''' 
❌ <b>CẢNH BÁO PHẠM VI</b> 
<blockquote>» Bạn chỉ được phép dùng Bot trong nhóm: 
» https://t.me/spamsmsquanghau</blockquote>''', parse_mode="HTML") 
        return 
         
    if bot_active == False and message.from_user.id != ADMIN_ID: 
        bot.send_message(message.chat.id, f''' 
❌ <b>HỆ THỐNG TẠM NGƯNG</b> 
<blockquote>» BOT hiện đang OFF để bảo trì.</blockquote>''', parse_mode="HTML") 
        return 
         
    user_id = message.from_user.id 
     
    # 3. KIỂM TRA QUYỀN SUPER VIP 
    if not check_super_status(user_id): 
        bot.send_message(message.chat.id, f''' 
❌ <b>QUYỀN HẠN KHÔNG ĐỦ</b> 
<blockquote>» Lệnh này chỉ dành cho tài khoản <b>SUPER VIP</b>. 
» Vui lòng liên hệ Admin để nâng cấp.</blockquote>''', parse_mode="HTML") 
        return 
 
    # 4. KIỂM TRA THAM SỐ SĐT 
    params = message.text.split()[1:] 
    if len(params) != 1: 
        msg = bot.send_message(message.chat.id, f''' 
⚠️ <b>SAI ĐỊNH DẠNG</b> 
<blockquote>» Cú pháp: <code>/callvip SĐT</code></blockquote>''', parse_mode="HTML") 
        threading.Timer(5, lambda: bot.delete_message(message.chat.id, msg.message_id)).start() 
        return 
 
    sdt = params[0] 
    if not sdt.isdigit() or len(sdt) != 10: 
        bot.send_message(message.chat.id, "❌ <b>SĐT Không Hợp Lệ</b>", parse_mode="HTML") 
        return 
 
    # 5. KIỂM TRA BLACKLIST VÀ ĐANG CHẠY 
    if sdt in blacklist: 
        bot.send_message(message.chat.id, f''' 
» Á À Tao Bắt Quả Tang Nhóc Spam Blacklist Nhé 
┌───⭓ 
<blockquote>» {message.from_user.full_name}</blockquote> 
└───⧕''', parse_mode="HTML") 
        return 
 
    if sdt in spam_processes: 
        bot.send_message(message.chat.id, f"❌ <b>SĐT {mask_sdt(sdt)} Đang Chạy!</b>", parse_mode="HTML") 
        return 
     
    # 6. KIỂM TRA COOLDOWN 30S 
    current_time = time.time() 
    if user_id in last_usage and current_time - last_usage[user_id] < 30: 
        remaining = 30 - (current_time - last_usage[user_id]) 
        bot.send_message(message.chat.id, f"❌ <b>Chờ {remaining:.0f}s nữa để tiếp tục.</b>", parse_mode="HTML") 
        return 
    last_usage[user_id] = current_time 
 
    # LẤY THÔNG TIN HIỂN THỊ 
    network_provider = get_network_provider(sdt) 
    masked_phone = mask_sdt(sdt) 
    formatted_time = time.strftime("%H:%M:%S, %d/%m/%Y") 
     
    loading = bot.send_message(message.chat.id, '⏳') 
 
    def spam_task(): 
        script_filename = "nat1.py" 
        if os.path.isfile(script_filename): 
            # Khởi tạo trạng thái đang chạy 
            spam_processes[sdt] = "STARTING" 
            spam_users[sdt] = user_id 
             
            try: bot.delete_message(message.chat.id, loading.message_id) 
            except: pass 
             
            bot.send_message(message.chat.id, f''' 
┌───⭓ <b>CALL VIP STARTED</b> 
<blockquote>» Target: [{masked_phone}] 
» Nhà Mạng: [{network_provider}] 
» Gói: [SUPER VIP] 
» Lúc: [{formatted_time}]</blockquote> 
<b>Lệnh Dừng:</b> <code>/stopcallvip {sdt}</code> 
└───⧕''', parse_mode="HTML") 
 
            # --- CHẠY FILE 1 LẦN DUY NHẤT --- 
            process = subprocess.Popen(["python", script_filename, sdt, "10"]) 
            spam_processes[sdt] = process 
             
            process.wait() # Đợi file chạy xong 
             
            # Dọn dẹp sau khi hoàn thành 
            if sdt in spam_processes: del spam_processes[sdt] 
            if sdt in spam_users: del spam_users[sdt] 
        else: 
            bot.send_message(message.chat.id, "❌ Tập tin nat1.py không tồn tại.") 
             
    threading.Thread(target=spam_task).start() 
     
@bot.message_handler(commands=['stopcallvip']) 
def stop_callvip_specific(message): 
    # 1. XÓA TIN NHẮN LỆNH CỦA NGƯỜI DÙNG 
    try: 
        bot.delete_message(message.chat.id, message.message_id) 
    except: 
        pass 
 
    # 2. KIỂM TRA QUYỀN HẠN NHÓM HOẶC ADMIN 
    if message.chat.id != allowed_group_id and message.from_user.id != ADMIN_ID: 
        return 
 
    params = message.text.split()[1:] 
    if len(params) != 1: 
        msg = bot.send_message(message.chat.id, "⚠️ <b>SAI ĐỊNH DẠNG</b>\n<blockquote>» Cú pháp: <code>/stopcallvip SĐT</code></blockquote>", parse_mode="HTML") 
        threading.Timer(5, lambda: bot.delete_message(message.chat.id, msg.message_id)).start() 
        return 
 
    sdt = params[0] 
    masked_phone = mask_sdt(sdt) 
 
    # 3. KIỂM TRA XEM SĐT CÓ TRONG DANH SÁCH ĐANG CHẠY KHÔNG 
    if sdt in spam_processes: 
        user_who_started = spam_users.get(sdt) 
         
        # Chỉ Admin hoặc người tạo lệnh mới được dừng 
        if message.from_user.id == user_who_started or message.from_user.id == ADMIN_ID: 
            try: 
                process = spam_processes[sdt] 
                 
                # Nếu tiến trình đang thực sự chạy (không phải đang ở trạng thái chờ "STARTING") 
                if process and not isinstance(process, str): 
                    process.terminate()  # Ngắt file nat1.py 
                 
                # Dọn dẹp biến hệ thống 
                spam_processes.pop(sdt, None) 
                spam_users.pop(sdt, None) 
                 
                bot.send_message(message.chat.id, f''' 
✅ <b>DỪNG CALL VIP THÀNH CÔNG</b> 
┌───⭓ 
<blockquote>» Target: [{masked_phone}] 
» Trạng thái: Đã ngắt máy chủ 
» Dừng Bởi: {message.from_user.full_name}</blockquote> 
└───⧕''', parse_mode="HTML") 
            except Exception as e: 
                bot.send_message(message.chat.id, f"❌ Lỗi khi dừng: {e}") 
        else: 
            bot.send_message(message.chat.id, f"❌ <b>QUYỀN HẠN:</b>\n» Bạn không phải người khởi tạo lệnh cho số <code>{masked_phone}</code>", parse_mode="HTML") 
    else: 
        bot.send_message(message.chat.id, f"❌ <b>THÔNG BÁO:</b>\n» Số <code>{masked_phone}</code> hiện không chạy Call VIP.", parse_mode="HTML") 
 
@bot.message_handler(commands=['aotu']) 
def add_auto(message): 
    # 1. XÓA TIN NHẮN LỆNH 
    try: bot.delete_message(message.chat.id, message.message_id) 
    except: pass 
 
    user_id = message.from_user.id 
    user_username = message.from_user.username if message.from_user.username else "NoUsername" 
     
    # 2. Kiểm tra quyền VIP 
    if not check_super_status(user_id): 
        bot.send_message(message.chat.id, f''' 
❌ <b>QUYỀN HẠN KHÔNG ĐỦ</b> 
<blockquote>» Lệnh này chỉ dành cho tài khoản <b>SUPER VIP</b>. 
» Vui lòng liên hệ Admin để nâng cấp.</blockquote>''', parse_mode="HTML") 
        return 
 
    # 3. Kiểm tra định dạng lệnh 
    params = message.text.split()[1:] 
    if len(params) != 1: 
        msg = bot.send_message(message.chat.id, f''' 
» SAI ĐỊNH DẠNG!!! 
<blockquote>» /aotu + SĐT 
» VD: /aotu 0987654321</blockquote>''', parse_mode="HTML") 
        threading.Timer(5, lambda: bot.delete_message(message.chat.id, msg.message_id)).start() 
        return 
 
    sdt = params[0] 
    if not sdt.isdigit() or len(sdt) != 10: 
        bot.send_message(message.chat.id, "❌ SĐT Không Hợp Lệ (Phải là 10 chữ số)") 
        return 
 
    # 4. Kiểm tra Blacklist 
    if sdt in blacklist: 
        bot.send_message(message.chat.id, f''' 
» Á À Tao Bắt Quả Tang Nhóc Spam Blacklist Nhé 
┌───⭓ 
<blockquote>» {message.from_user.full_name}</blockquote> 
└───⧕''', parse_mode="HTML") 
        return 
 
    # 5. Kiểm tra trùng lặp 
    data = load_auto_data() 
    if sdt in data: 
        bot.send_message(message.chat.id, f"❌ Số <code>{mask_sdt(sdt)}</code> đã có trong danh sách tự động rồi!", parse_mode="HTML") 
        return 
 
    # 6. Lưu vào hệ thống 
    data[sdt] = user_id 
    save_auto_data(data) 
     
    bot.send_message(message.chat.id, f''' 
✅ <b>ĐÃ THÊM TỰ ĐỘNG THÀNH CÔNG</b> 
┌───⭓ 
<blockquote>» Target: <code>{mask_sdt(sdt)}</code> 
» Lịch chạy: 00:00 & 06:00 hằng ngày 
» Gói: [SUPERVIP] 
» Người thêm: {message.from_user.full_name}</blockquote> 
└───⧕ 
<i>Hệ thống sẽ tự động chạy đúng thời gian.</i>''', parse_mode="HTML") 
 
@bot.message_handler(commands=['listaotu']) 
def list_auto(message): 
    try: bot.delete_message(message.chat.id, message.message_id) 
    except: pass 
 
    user_id = message.from_user.id 
    if not check_super_status(user_id): 
        bot.send_message(message.chat.id, f''' 
❌ <b>QUYỀN HẠN KHÔNG ĐỦ</b> 
<blockquote>» Lệnh này chỉ dành cho tài khoản <b>SUPER VIP</b>. 
» Vui lòng liên hệ Admin để nâng cấp.</blockquote>''', parse_mode="HTML") 
        return 
 
    data = load_auto_data() 
    if not data: 
        bot.send_message(message.chat.id, "📋 Danh sách tự động hiện đang trống.") 
        return 
 
    if user_id == ADMIN_ID: 
        lines = [f"» <code>{mask_sdt(s)}</code> (ID: {u})" for s, u in data.items()] 
        title = "📋 TẤT CẢ SỐ CHẠY TỰ ĐỘNG (ADMIN)" 
    else: 
        user_numbers = [s for s, u in data.items() if u == user_id] 
        if not user_numbers: 
            bot.send_message(message.chat.id, "❓ Bạn chưa thêm số nào vào danh sách tự động.") 
            return 
        lines = [f"» <code>{mask_sdt(s)}</code>" for s in user_numbers] 
        title = "📋 DANH SÁCH TỰ ĐỘNG CỦA BẠN" 
 
    response = f"<b>{title}</b>\n<blockquote>" + "\n".join(lines) + "</blockquote>" 
    bot.send_message(message.chat.id, response, parse_mode="HTML") 
 
@bot.message_handler(commands=['xoaaotu']) 
def del_auto(message): 
    try: bot.delete_message(message.chat.id, message.message_id) 
    except: pass 
 
    user_id = message.from_user.id 
    params = message.text.split()[1:] 
    if len(params) != 1: 
        msg = bot.send_message(message.chat.id, "» Cú pháp: <code>/xoaaotu [SĐT]</code> hoặc <code>/xoaaotu all</code>", parse_mode="HTML") 
        threading.Timer(5, lambda: bot.delete_message(message.chat.id, msg.message_id)).start() 
        return 
 
    target = params[0].lower() 
    data = load_auto_data() 
 
    if target == 'all': 
        if user_id == ADMIN_ID: 
            save_auto_data({}) 
            bot.send_message(message.chat.id, "🗑️ <b>ADMIN:</b> Đã xóa sạch toàn bộ danh sách tự động!", parse_mode="HTML") 
        else: 
            bot.send_message(message.chat.id, "❌ Chỉ Admin mới có quyền xóa tất cả!") 
        return 
 
    if target in data: 
        if data[target] == user_id or user_id == ADMIN_ID: 
            masked = mask_sdt(target) 
            del data[target] 
            save_auto_data(data) 
            bot.send_message(message.chat.id, f"✅ Đã xóa số <code>{masked}</code> khỏi danh sách tự động.", parse_mode="HTML") 
        else: 
            bot.send_message(message.chat.id, "❌ Bạn không có quyền xóa số này!") 
    else: 
        bot.send_message(message.chat.id, "❌ Số này không có trong danh sách tự động.") 
     
@bot.message_handler(commands=['stop']) 
def stop_spam(message): 
    # 1. XÓA TIN NHẮN LỆNH CỦA NGƯỜI DÙNG 
    try: 
        bot.delete_message(message.chat.id, message.message_id) 
    except: 
        pass 
 
    if message.chat.id != allowed_group_id: 
        bot.send_message(message.chat.id, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
 
    params = message.text.split()[1:] 
    if len(params) != 1: 
        msg = bot.send_message(message.chat.id, f''' 
» SAI ĐỊNH DẠNG!!! 
<blockquote>» /stop + SĐT 
» VD: /stop 0987654321</blockquote> 
    ''', parse_mode="HTML") 
        # Tự xóa thông báo lỗi sau 5 giây 
        threading.Timer(5, lambda: bot.delete_message(message.chat.id, msg.message_id)).start() 
        return 
 
    # XỬ LÝ LỆNH STOP ALL (ADMIN ONLY) 
    if params[0] == "all": 
        if message.from_user.id == ADMIN_ID: 
            if not spam_processes: 
                bot.send_message(message.chat.id, '✅ Hiện Tại Không Có SĐT Nào Đang Spam') 
                return 
            count = len(spam_processes) 
            for sdt, process in list(spam_processes.items()): 
                process.terminate() 
                del spam_processes[sdt] 
                if sdt in spam_users: del spam_users[sdt] 
            bot.send_message(message.chat.id, f'✅ <b>ADMIN:</b> Đã Ngừng Tất Cả {count} Luồng Đang Spam!') 
            return 
        else: 
            bot.send_message(message.chat.id, '❌ Mày Đéo Có Quyền Sử Dụng Lệnh Này Đâu, Chỉ QuanghauDz Mới Có Quyền Ra Lệnh STOP ALL') 
            return 
 
    sdt = params[0] 
    masked_phone = mask_sdt(sdt) # ẨN SỐ ĐIỆN THOẠI 
 
    if sdt in spam_processes: 
        if sdt in spam_users: 
            # KIỂM TRA QUYỀN (CHÍNH CHỦ HOẶC ADMIN) 
            if message.from_user.id == spam_users[sdt] or message.from_user.id == ADMIN_ID: 
                process = spam_processes[sdt] 
                process.terminate() 
                del spam_processes[sdt] 
                del spam_users[sdt] 
                bot.send_message(message.chat.id, f'✅ Đã Ngừng Spam SĐT [<code>{masked_phone}</code>]', parse_mode="HTML") 
            else: 
                bot.send_message(message.chat.id, f'❌ Chỉ Chính Người Spam [<code>{masked_phone}</code>] Mới Có Thể Stop Tại Server Spam VIP', parse_mode="HTML") 
        else: 
            # Trường hợp số chạy tự động hoặc không rõ người khởi tạo 
            process = spam_processes[sdt] 
            process.terminate() 
            del spam_processes[sdt] 
            bot.send_message(message.chat.id, f'✅ Đã Ngừng Spam SĐT [<code>{masked_phone}</code>]', parse_mode="HTML") 
    else: 
        bot.send_message(message.chat.id, f'❌ [<code>{masked_phone}</code>] Không Tồn Tại Trong Danh Sách Đang Spam', parse_mode="HTML") 
 
@bot.message_handler(commands=['start']) 
def start(message): 
    user_id = message.from_user.id 
    args = message.text.split() 
    referrer_name = "một người bạn" 
 
    if len(args) > 1: 
        # --- TRƯỜNG HỢP 1: XÁC THỰC ĐỂ LẤY LINK MỜI --- 
        if args[1] == "verify_share": 
            # Kiểm tra VIP hoặc SUPER VIP trước khi nhả link 
            if (user_id in allowed_users and check_vip_status(user_id)) or check_super_status(user_id): 
                bot.reply_to(message, "❌ Bạn đã có quyền VIP/SUPER VIP rồi, không cần dùng link mời nữa.") 
                return 
             
            bot_username = bot.get_me().username 
            ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}" 
            count = referrals.get(str(user_id), 0) 
             
            bot.reply_to(message, f''' 
✅ <b>XÁC THỰC THÀNH CÔNG</b> 
┌───⭓ 
<blockquote>» Link mời của bạn: <code>{ref_link}</code> 
» Tiến độ: [{count}/5] Người 
» Phần thưởng: 7 ngày VIP</blockquote> 
└───⧕ 
<i>Hãy gửi link này cho bạn bè, đủ 5 người bạn sẽ nhận VIP tự động!</i> 
            ''', parse_mode="HTML") 
            return 
 
        # --- TRƯỜNG HỢP 2: ĐƯỢC NGƯỜI KHÁC MỜI VÀO (ref_ID) --- 
        if args[1].startswith('ref_'): 
            try: 
                referrer_id = int(args[1].replace('ref_', '')) 
                 
                try: 
                    ref_info = bot.get_chat(referrer_id) 
                    referrer_name = f"@{ref_info.username}" if ref_info.username else ref_info.first_name 
                except: 
                    pass 
 
                if user_id not in joined_users and referrer_id != user_id: 
                    referrals[str(referrer_id)] = referrals.get(str(referrer_id), 0) + 1 
                    current_points = referrals[str(referrer_id)] 
 
                    try: 
                        bot.send_message(referrer_id, f''' 
📩 <b>CÓ NGƯỜI ẤN VÀO LINK MỜI CỦA BẠN!</b> 
┌───⭓ 
<blockquote>» Người tham gia: <b>{message.from_user.full_name}</b> 
» Tiến độ: <b>{current_points}/5</b> người</blockquote> 
└───⧕ 
<i>Còn {5 - current_points} người nữa để nhận VIP!</i>''', parse_mode="HTML") 
                    except: pass 
 
                    if referrals[str(referrer_id)] >= 5: 
                        referrals[str(referrer_id)] = 0 
                        now = time.time() 
                         
                        # Ưu tiên cộng vào VIP thường, không can thiệp SUPER VIP 
                        current_expire = user_keys.get(referrer_id, now) 
                        if current_expire != "permanent": 
                            new_expire = max(float(current_expire), now) + 604800 
                            user_keys[referrer_id] = new_expire 
                            allowed_users.add(referrer_id) 
                            save_vip_users() 
                            try: 
                                bot.send_message(referrer_id, "🎉 <b>CHÚC MỪNG!</b>\n<blockquote>Bạn đã mời đủ 5 người và được cộng 7 ngày VIP. Cảm ơn vì đã mời người mới!</blockquote>", parse_mode="HTML") 
                            except: pass 
                     
                    save_data(REF_FILE, referrals) 
            except Exception as e: 
                print(f"Lỗi xử lý ref: {e}") 
 
    if user_id not in joined_users: 
        joined_users.append(user_id) 
        save_data(JOINED_USERS_FILE, joined_users) 
 
    welcome_msg = f''' 
👋 <b>CHÀO MỪNG NGƯỜI MỚI</b> 
┌───⭓ 
<blockquote>» Bạn: <b>{message.from_user.full_name}</b> 
» Được mời bởi: <b>{referrer_name}</b> 
» Trạng thái: Đã tham gia hệ thống!</blockquote> 
└───⧕ 
<i>Hãy gõ /bot để xem danh sách lệnh của Bot nhé.</i> 
''' 
    bot.reply_to(message, welcome_msg, parse_mode="HTML") 
 
@bot.message_handler(commands=['share']) 
def share_link(message): 
    user_id = message.from_user.id 
    bot_username = bot.get_me().username 
 
    # Kiểm tra cả VIP thường và SUPER VIP 
    is_vip = (user_id in allowed_users and check_vip_status(user_id)) 
    is_super = check_super_status(user_id) 
 
    if is_vip or is_super: 
        bot.reply_to(message, f''' 
❌ <b>THÔNG BÁO</b> 
<blockquote>Bạn đang có quyền {"SUPER VIP" if is_super else "VIP"}, không thể sử dụng link mời để nhận thêm.</blockquote> 
        ''', parse_mode="HTML") 
        return 
 
    verify_link = f"https://t.me/{bot_username}?start=verify_share" 
     
    bot.reply_to(message, f''' 
⚠️ <b>XÁC THỰC YÊU CẦU</b> 
┌───⭓ 
<blockquote>Để lấy link giới thiệu, bạn vui lòng nhấn vào link dưới đây để hệ thống xác nhận:</blockquote> 
└───⧕ 
👉 <a href="{verify_link}">NHẤN VÀO ĐÂY ĐỂ LẤY LINK</a> 
''', parse_mode="HTML", disable_web_page_preview=True) 
 
@bot.message_handler(commands=['full']) 
def spam_full_vip(message): 
    # 1. XÓA TIN NHẮN LỆNH CỦA NGƯỜI DÙNG 
    try: 
        bot.delete_message(message.chat.id, message.message_id) 
    except: 
        pass 
 
    user_id = message.from_user.id 
    full_name = message.from_user.full_name 
     
    # 2. Kiểm tra quyền VIP và trạng thái VIP 
    if not check_super_status(user_id): 
        bot.send_message(message.chat.id, f''' 
❌ <b>QUYỀN HẠN KHÔNG ĐỦ</b> 
<blockquote>» Lệnh này chỉ dành cho tài khoản <b>SUPER VIP</b>. 
» Vui lòng liên hệ Admin để nâng cấp.</blockquote>''', parse_mode="HTML") 
        return 
 
    # 3. Kiểm tra tham số SĐT 
    params = message.text.split()[1:] 
    if len(params) != 1: 
        msg = bot.send_message(message.chat.id, f''' 
⚠️ <b>SAI ĐỊNH DẠNG</b> 
<blockquote>» Cú pháp: <code>/full SĐT</code> 
» VD: <code>/full 0987654321</code></blockquote>''', parse_mode="HTML") 
        threading.Timer(5, lambda: bot.delete_message(message.chat.id, msg.message_id)).start() 
        return 
 
    sdt = params[0].strip() 
     
    # 4. Kiểm tra tính hợp lệ và Blacklist 
    if not sdt.isdigit() or len(sdt) != 10: 
        bot.send_message(message.chat.id, "❌ Số điện thoại không hợp lệ.") 
        return 
 
    if sdt in blacklist: 
        bot.send_message(message.chat.id, f''' 
» Á À Tao Bắt Quả Tang Nhóc Spam Blacklist Nhé 
┌───⭓ 
<blockquote>» {message.from_user.full_name}</blockquote> 
└───⧕''', parse_mode="HTML") 
        return 
 
    # 5. Kiểm tra Cooldown 30s 
    current_time = time.time() 
    if user_id in last_usage and current_time - last_usage[user_id] < 30: 
        remaining = 30 - (current_time - last_usage[user_id]) 
        bot.send_message(message.chat.id, f"❌ Thích Spam Lắm Không? {remaining:.0f} Giây Nữa Nhé") 
        return 
 
    # 6. Gửi thông báo tấn công 
    network_provider = get_network_provider(sdt) 
    masked_phone = mask_sdt(sdt) 
    formatted_time = time.strftime("%H:%M:%S %d/%m/%Y") 
    sms_count = 10 # Số lần cho file dec.py 
 
    final_msg = f''' 
┌───⭓ 
<blockquote>» Name: {message.from_user.full_name}</blockquote> 
└───⧕ 
┌───⭓ 
<blockquote>» Server: Tấn Công Tổng Lực (Sms + Call) 
» Target: [{masked_phone}] 
» Sms: [{sms_count} lần] 
» Call: [5 call] 
» Gói: [SUPER VIP] 
» Lúc: [{formatted_time}] 
» Dừng: [/stopfull {sdt}]</blockquote> 
└───⧕''' 
    bot.send_message(message.chat.id, final_msg, parse_mode="HTML") 
 
    # 7. Khởi chạy đa luồng 
    def run_full_attack(): 
        try: 
            # CHẠY FILE DEC.PY (Sms) 
            p_sms = subprocess.Popen(['python', 'dec.py', sdt, str(sms_count)]) 
             
            # Lưu vào bộ nhớ để có thể dừng 
            if user_id not in full_spam_processes: 
                full_spam_processes[user_id] = {} 
            full_spam_processes[user_id][sdt] = [p_sms] 
             
            last_usage[user_id] = current_time  
 
            # --- CHẠY FILE NAT1.PY 1 LẦN DUY NHẤT (Call) --- 
            p_call = subprocess.Popen(['python', 'nat1.py', sdt, "5"]) 
            full_spam_processes[user_id][sdt].append(p_call) 
             
            # Đợi cả 2 tiến trình hoàn thành 
            p_sms.wait() 
            p_call.wait() 
             
            # Sau khi xong thì dọn dẹp 
            if user_id in full_spam_processes and sdt in full_spam_processes[user_id]: 
                del full_spam_processes[user_id][sdt] 
 
        except Exception as e: 
            print(f"Lỗi khởi chạy Full: {e}") 
 
    threading.Thread(target=run_full_attack).start() 
 
# --- LỆNH /STOPFULL --- 
@bot.message_handler(commands=['stopfull']) 
def stop_full_spam(message): 
    # 1. XÓA TIN NHẮN LỆNH CỦA NGƯỜI DÙNG 
    try: 
        bot.delete_message(message.chat.id, message.message_id) 
    except: 
        pass 
 
    user_id = message.from_user.id 
    params = message.text.split()[1:] 
     
    if len(params) != 1: 
        msg = bot.send_message(message.chat.id, "⚠️ <b>SAI ĐỊNH DẠNG</b>\n<blockquote>» Nhập SĐT cần dừng. VD: <code>/stopfull 0987654321</code></blockquote>", parse_mode="HTML") 
        threading.Timer(5, lambda: bot.delete_message(message.chat.id, msg.message_id)).start() 
        return 
 
    sdt = params[0].strip() 
    masked_phone = mask_sdt(sdt) 
 
    # 2. TÌM KIẾM TIẾN TRÌNH TRÊN TOÀN HỆ THỐNG 
    # Kiểm tra xem SĐT này có ai đang chạy không 
    target_uid = None 
    for uid in full_spam_processes: 
        if sdt in full_spam_processes[uid]: 
            target_uid = uid 
            break 
 
    if not target_uid: 
        bot.send_message(message.chat.id, f"❌ <b>THÔNG BÁO</b>\n<blockquote>» Mục tiêu <code>{masked_phone}</code> hiện không có luồng /full nào đang chạy.</blockquote>", parse_mode="HTML") 
        return 
 
    # 3. KIỂM TRA QUYỀN (Chỉ Admin hoặc người tạo lệnh mới được dừng) 
    if user_id != ADMIN_ID and user_id != target_uid: 
        bot.send_message(message.chat.id, f"❌ <b>TRUY CẬP BỊ TỪ CHỐI</b>\n<blockquote>» Bạn không có quyền dừng mục tiêu của người khác.</blockquote>", parse_mode="HTML") 
        return 
 
    # 4. TIẾN HÀNH DỪNG TẤT CẢ LUỒNG (Sms + Call) 
    try: 
        processes = full_spam_processes[target_uid][sdt] # Đây là list [p_sms, p_call] 
         
        for p in processes: 
            try: 
                # Kiểm tra nếu p là object subprocess và đang chạy 
                if hasattr(p, 'poll') and p.poll() is None: 
                    p.terminate()  
                    p.wait(timeout=1) # Đợi 1s để tiến trình đóng hẳn 
            except: 
                pass 
         
        # Dọn dẹp bộ nhớ 
        del full_spam_processes[target_uid][sdt] 
        if not full_spam_processes[target_uid]: 
            del full_spam_processes[target_uid] 
 
        bot.send_message(message.chat.id, f''' 
✅ <b>DỪNG TỔNG LỰC THÀNH CÔNG</b> 
┌───⭓ 
<blockquote>» Target: [{masked_phone}] 
» Trạng thái: Đã ngắt toàn bộ Sms & Call 
» Dừng Bởi: {message.from_user.full_name}</blockquote> 
└───⧕''', parse_mode="HTML") 
 
    except Exception as e: 
        bot.send_message(message.chat.id, f"❌ <b>LỖI:</b> {e}") 
     
@bot.message_handler(commands=['status']) 
def status(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
 
    if not spam_processes: 
        bot.reply_to(message, '✅ Không Có SĐT Nào Đang Được Spam') 
        return 
 
    active_spams = "\n".join(spam_processes.keys()) 
    bot.reply_to(message, f'✅ Danh Sách Các SĐT Đang Spam:\n<blockquote>{active_spams}</blockquote>', parse_mode="HTML") 
 
@bot.message_handler(commands=['uservip']) 
def uservip(message): 
    if message.chat.id != allowed_group_id: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
 
    if os.path.exists('vip_users.json'): 
        with open('vip_users.json', 'r') as f: 
            vip_data = json.load(f) 
        if not vip_data: 
            bot.reply_to(message, '✅ Hiện Tại Không Có User VIP') 
            return 
         
        total_vip_users = len(vip_data) 
        response_message = f"👤 <b>Danh Sách User Vip</b> 👤\n👀 Hiện Tại Đang Có {total_vip_users} User VIP\n\n" 
 
        for user_id, status in vip_data.items(): 
            if status == "permanent": 
                expiration_message = "VIP Vĩnh Viễn" 
                countdown = "Vô thời hạn" 
            else: 
                expiration_time_readable = time.strftime("%H:%M:%S, %d/%m/%Y", time.localtime(float(status))) 
                expiration_message = f"Hết Hạn Lúc: {expiration_time_readable}" 
                # Gọi hàm tính số ngày còn lại 
                countdown = get_remaining_days_vip(status) 
 
            # Hiển thị thêm dòng countdown vào blockquote 
            response_message += f''' 
<blockquote>» ID [{user_id}] 
» {expiration_message} 
» {countdown}</blockquote> 
''' 
 
        bot.reply_to(message, response_message, parse_mode="HTML") 
    else: 
        bot.reply_to(message, '❌ Không Tìm Thấy Tệp Dữ Liệu VIP.') 
 
@bot.message_handler(commands=['usersuper']) 
def list_super_users(message): 
    if message.from_user.id != ADMIN_ID: # Hoặc kiểm tra nhóm tùy bạn 
        return 
 
    if not super_users: 
        bot.reply_to(message, "<b>❌ Hiện tại chưa có tài khoản SUPER VIP nào.</b>", parse_mode="HTML") 
        return 
 
    text = "👑 <b>DANH SÁCH SUPER VIP</b>\n" 
    text += "────────────────────\n" 
     
    count = 1 
    for user_id in list(super_users): 
        if check_super_status(user_id): # Kiểm tra hạn dùng 
            status = super_keys.get(user_id) 
            time_left = get_remaining_days(status) # Gọi hàm tính ngày ở Bước 2 
            text += f"{count}. ID: <code>{user_id}</code>\n" 
            text += f"   » Còn lại: <b>{time_left}</b>\n" 
            count += 1 
     
    text += "────────────────────\n" 
    text += f"Tổng cộng: {count-1} tài khoản." 
    bot.send_message(message.chat.id, text, parse_mode="HTML") 
     
# Lệnh xem danh sách người bị Mute (từ file muted_users.json) 
@bot.message_handler(commands=['list']) 
def list_muted(message): 
    if message.chat.id != allowed_group_id and message.from_user.id != ADMIN_ID: 
        return 
     
    file_path = 'muted_users.json' 
    if os.path.exists(file_path): 
        with open(file_path, 'r', encoding='utf-8') as f: 
            try: 
                data = json.load(f) 
                # Nếu data là danh sách ID 
                if data: 
                    msg = "<b>=== DANH SÁCH NGƯỜI BỊ MUTE ===</b>\n" 
                    for idx, user_id in enumerate(data, 1): 
                        msg += f"{idx}. ID: <code>{user_id}</code>\n" 
                    bot.reply_to(message, msg, parse_mode="HTML") 
                else: 
                    bot.reply_to(message, "✅ Danh sách Mute hiện đang trống.") 
            except: 
                bot.reply_to(message, "❌ Lỗi khi đọc file muted_users.json") 
    else: 
        bot.reply_to(message, "❌ File muted_users.json không tồn tại.") 
 
# Lệnh xem danh sách SĐT cấm (từ file blacklist.json) 
@bot.message_handler(commands=['listsdt']) 
def list_sdt_blacklist(message): 
    if message.chat.id != allowed_group_id and message.from_user.id != ADMIN_ID: 
        return 
 
    file_path = 'blacklist.json' 
    if os.path.exists(file_path): 
        with open(file_path, 'r', encoding='utf-8') as f: 
            try: 
                data = json.load(f) 
                if data: 
                    msg = "<b>=== DANH SÁCH SĐT CẤM (BLACKLIST) ===</b>\n" 
                    # Chỉ hiện 50 số đầu để tránh quá tải tin nhắn Telegram 
                    for idx, sdt in enumerate(data[:50], 1): 
                        msg += f"{idx}. <code>{sdt}</code>\n" 
                     
                    if len(data) > 50: 
                        msg += f"\n<i>... và {len(data) - 50} số khác.</i>" 
                    bot.reply_to(message, msg, parse_mode="HTML") 
                else: 
                    bot.reply_to(message, "✅ Danh sách SĐT cấm hiện đang trống.") 
            except: 
                bot.reply_to(message, "❌ Lỗi khi đọc file blacklist.json") 
    else: 
        bot.reply_to(message, "❌ File blacklist.json không tồn tại.") 
         
BLACKLIST_FILE = 'blacklist.json' 
 
def load_blacklist(): 
    global blacklist 
    if os.path.exists(BLACKLIST_FILE): 
        with open(BLACKLIST_FILE, 'r') as f: 
            blacklist = json.load(f) 
 
def save_blacklist(): 
    with open(BLACKLIST_FILE, 'w') as f: 
        json.dump(blacklist, f) 
 
@bot.message_handler(commands=['addblacklist']) 
def add_to_blacklist(message): 
    if message.chat.id != ALLOWED_GROUP_ID: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
 
    if message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ Mày Đéo Có Quyền Sử Dụng Lệnh Này Đâu, Chỉ QuanghauDz Mới Có Quyền Ra Lệnh Blacklist') 
        return 
 
    params = message.text.split()[1:] 
 
    sdt = params[0] 
    if sdt in blacklist: 
        bot.reply_to(message, f'❌ SĐT [{sdt}] Đã Có Trong Danh Sách Blacklist') 
        return 
 
    blacklist.append(sdt) 
    save_blacklist() 
    bot.reply_to(message, f'✅ Đã Thêm SĐT [{sdt}] Vào Danh Sách Blacklist') 
 
@bot.message_handler(commands=['delblacklist']) 
def remove_from_blacklist(message): 
    if message.chat.id != ALLOWED_GROUP_ID: 
        bot.reply_to(message, '❌ Bạn Chỉ Được Phép Dùng Bot Trong https://t.me/spamsmsquanghau') 
        return 
 
    if message.from_user.id != ADMIN_ID: 
        bot.reply_to(message, '❌ Mày Đéo Có Quyền Sử Dụng Lệnh Này Đâu, Chỉ QuanghauDz Mới Có Quyền Ra Lệnh Reset') 
        return 
 
    params = message.text.split()[1:] 
 
    sdt = params[0] 
    if sdt not in blacklist: 
        bot.reply_to(message, f'❌ SĐT [{sdt}] Không Có Trong Danh Sách Blacklist') 
        return 
 
    blacklist.remove(sdt) 
    save_blacklist() 
    bot.reply_to(message, f'✅ Đã Xóa SĐT [{sdt}] Khỏi Danh Sách Blacklist') 
 
@bot.message_handler(func=lambda message: True) 
def handle_all_messages(message): 
    if message.text.startswith('/'): 
        if not is_valid_command(message.text): 
            bot.reply_to(message, '❌ Lệnh Không Hợp Lệ, Vui Lòng Sử Dụng /bot Để Hiển Thị Các Lệnh') 
 
def is_valid_command(command): 
    # Lấy từ đầu tiên (ví dụ: /spam 09xxx -> lấy /spam) 
    # Chuyển về chữ thường để tránh lỗi khi người dùng gõ chữ HOA 
    cmd = command.split()[0].lower() 
     
    # Danh sách các lệnh hợp lệ CÓ DẤU / 
    valid_commands = [ 
        '/uservip', '/status', '/stop', '/key', '/addvip',  
        '/delvip', '/ping', '/off', '/on', '/mute',  
        '/bot', '/muavip', '/warning', '/admin', '/checkme',  
        '/reset', '/spam', '/spamvip', # Cặp lệnh Call Free 
        '/callvip', '/stopcallvip',     # Cặp lệnh Call VIP 
        '/unmute', '/ban', '/unban', '/list', '/listsdt', '/taokey', '/aotu', '/listaotu', '/xoaaotu', '/start', '/share', '/full', '/stopfull', '/usersuper' # Cặp lệnh 24h VIP 
    ] 
     
    return cmd in valid_commands 
 
def check_and_notify_expired(): 
    now = time.time() 
     
    # 1. KIỂM TRA SUPER VIP 
    expired_super = [] 
    for user_id, status in list(super_keys.items()): 
        if status != "permanent" and now > float(status): 
            expired_super.append(user_id) 
     
    for uid in expired_super: 
        super_users.discard(uid) 
        super_keys.pop(uid, None) 
        save_super_users() 
        try: 
            bot.send_message(ALLOWED_GROUP_ID, f''' 
🔔 <b>THÔNG BÁO HẾT HẠN SUPER VIP</b> 
──────────────────── 
» Người dùng: <code>{message.from_user.full_name}</code> 
» Trạng thái: <b>Đã hết hạn</b> 
» Thông báo: Vui lòng liên hệ Admin để gia hạn tiếp tục sử dụng Các Lệnh Super. 
────────────────────''', parse_mode="HTML") 
        except: pass 
 
    # 2. KIỂM TRA VIP THƯỜNG (vip_users.json) 
    if os.path.exists('vip_users.json'): 
        try: 
            with open('vip_users.json', 'r') as f: 
                vip_data = json.load(f) 
             
            updated_vip = False 
            expired_vip = [] 
             
            for user_id, status in list(vip_data.items()): 
                if status != "permanent" and now > float(status): 
                    expired_vip.append(user_id) 
             
            for uid in expired_vip: 
                vip_data.pop(uid, None) 
                allowed_users.discard(int(uid)) 
                updated_vip = True 
                try: 
                    bot.send_message(ALLOWED_GROUP_ID, f''' 
🔔 <b>THÔNG BÁO HẾT HẠN VIP</b> 
──────────────────── 
» Người dùng: <code>{message.from_user.full_name}</code> 
» Trạng thái: <b>Đã hết hạn</b> 
» Thông báo: Quyền VIP của bạn đã kết thúc. Vui lòng liên hệ Admin để gia hạn. 
────────────────────''', parse_mode="HTML") 
                except: pass 
             
            if updated_vip: 
                with open('vip_users.json', 'w') as f: 
                    json.dump(vip_data, f) 
        except: pass 
 
# Hàm chạy vòng lặp kiểm tra mỗi 10 phút (hoặc tùy chỉnh) 
def expiration_scheduler(): 
    while True: 
        check_and_notify_expired() 
        time.sleep(60) # Kiểm tra sau mỗi 600 giây (10 phút) 
         
if __name__ == "__main__": 
    # KHÔNG khai báo lại allowed_users = set() ở đây vì nó sẽ xóa dữ liệu cũ 
    load_vip_users() 
    load_spam_counts() 
    load_blacklist() 
     
    # Khởi chạy các luồng kiểm tra chạy ngầm 
    threading.Thread(target=check_all_vip_status, daemon=True).start() 
    threading.Thread(target=check_muted_users_loop, daemon=True).start() 
    threading.Thread(target=vip, daemon=True).start() 
    threading.Thread(target=expiration_scheduler, daemon=True).start() 
     
    print("🤖 BOT ĐÃ SẴN SÀNG HOẠT ĐỘNG!") 
    bot.infinity_polling()         