import telebot
import requests
import random
import threading
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

TOKEN = "7722243309:AAE7qB9XHMSco9--u7-e_EwMO84T7lNqdcE"
bot = telebot.TeleBot(TOKEN)
lock = Lock()
user_locks = {}

link_api = f"https://visits-lk-tm-v2.vercel.app/28310049"
data = requests.get(link_api).json()
print(data)

if __name__ == '__main__':  
    bot.infinity_polling()