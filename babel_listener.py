import requests
import time
import os
import sqlite3
from deep_translator import GoogleTranslator

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or "7125906763"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def log_to_corpus(sender, original, sw, ar):
    try:
        conn = sqlite3.connect('ri_os_memory.db')
        cursor = conn.cursor()
        # Adding a column for Arabic in the metadata or a new schema
        cursor.execute('''
            INSERT INTO imperial_logs (sender_id, original_text, translated_text, metadata)
            VALUES (?, ?, ?, ?)
        ''', (sender, original, sw, f"Arabic: {ar}"))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Memory Error: {e}")

def translate_text(text, target):
    try:
        return GoogleTranslator(source='auto', target=target).translate(text)
    except:
        return "[Error]"

print("🏛️ RI-OS BABEL-BRIDGE: SW & ARABIC ONLINE")

last_update_id = None
while True:
    try:
        response = requests.get(URL + "getUpdates?timeout=10&offset=" + str(last_update_id if last_update_id else "")).json()
        if "result" in response:
            for update in response["result"]:
                last_update_id = update["update_id"] + 1
                if "message" in update and "text" in update["message"]:
                    user_text = update["message"]["text"]
                    
                    # Dual Translation
                    sw_text = translate_text(user_text, 'sw')
                    ar_text = translate_text(user_text, 'ar')
                    
                    log_to_corpus(update["message"]["from"]["id"], user_text, sw_text, ar_text)
                    
                    reply = (f"🏛️ RI-OS BRIDGE\n\n"
                             f"🇰🇪 SW: {sw_text}\n"
                             f"🇸🇦 AR: {ar_text}")
                    
                    requests.get(URL + f"sendMessage?chat_id={CHAT_ID}&text={reply}")
                    print(f"📡 Logged: {user_text[:15]}... [SW/AR]")
    except Exception as e:
        print(f"⚠️ Glitch: {e}")
    time.sleep(1)
