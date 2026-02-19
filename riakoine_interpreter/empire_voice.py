import os
import time
import sys
import json
import requests
from dotenv import load_dotenv
from difflib import get_close_matches

# --- LOAD SECRETS ---
load_dotenv()
EMERGENCY_CONTACT = os.getenv("EMERGENCY_CONTACT")
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- DICTIONARIES ---
SWAHILI_DICT = {
    "money": "Pesa", "profit": "Faida", "loss": "Hasara", "buy": "Nunua", "sell": "Uza", 
    "market": "Soko", "car": "Gari", "police": "Polisi", "doctor": "Daktari",
    "emergency": "Dharura", "water": "Maji", "food": "Chakula", "help": "Saidia"
}

ARABIC_DICT = {
    "money": "Fulus", "profit": "Ribh", "loss": "Khasara", "buy": "Ishtari", "sell": "Bee", 
    "market": "Souq", "car": "Sayyara", "police": "Shorta", "doctor": "Tabib",
    "emergency": "Tawari", "water": "Ma'a", "food": "Akl", "boss": "Mudir", "help": "Musa'ada",
    "hospital": "Mustashfa", "road": "Tariq", "mosque": "Masjid"
}

CURRENT_MODE = "sw" 

def speak_feedback(text):
    os.system(f"termux-tts-speak '{text}'")
    time.sleep(1.5)

def trigger_emergency(captured_text):
    """Vibrates and sends Telegram + SMS alerts"""
    print("\n[!!!] EMERGENCY ALERT TRIGGERED [!!!]")
    # Simplified vibration for better compatibility
    os.system("termux-vibrate -d 1000") 
    
    # 1. Telegram Alert
    if TG_TOKEN and TG_CHAT_ID:
        message = f"🚨 *EMERGENCY ALERT*\nUser said: '{captured_text}'\nContact: {EMERGENCY_CONTACT}"
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        try:
            requests.post(url, data={"chat_id": TG_CHAT_ID, "text": message, "parse_mode": "Markdown"})
            print("Telegram alert sent.")
        except Exception as e:
            print(f"Telegram failed: {e}")

    # 2. SMS Alert
    print(f"Attempting to SMS {EMERGENCY_CONTACT}...")
    sms_text = f"EMERGENCY: Riakoine Alert Triggered. Voice Captured: {captured_text}"
    # Using double quotes for the message to avoid shell issues
    os.system(f'termux-sms-send -n {EMERGENCY_CONTACT} "{sms_text}"')
    
    speak_feedback("Alert sent to your emergency contact.")

def listen_with_retry(retries=1):
    for attempt in range(retries + 1):
        os.system("termux-vibrate -d 50")
        voice = os.popen("termux-speech-to-text").read().strip().lower()
        if voice: return voice
    return ""

def main():
    global CURRENT_MODE
    os.system('clear')
    print(f"--- 🌍 RIAKOINE SECURE HUB (Contact: {EMERGENCY_CONTACT}) ---")
    speak_feedback("Security System Active.")

    try:
        while True:
            ACTIVE_DICT = SWAHILI_DICT.copy() if CURRENT_MODE == "sw" else ARABIC_DICT.copy()
            
            print(f"\n[ 👂 LISTENING... ]")
            voice = listen_with_retry(retries=2)
            if not voice: continue
            print(f"Captured: '{voice}'")

            # --- 🚨 EMERGENCY CHECK 🚨 ---
            if any(word in voice for word in ["emergency", "help", "saidia", "tulong", "tawari"]):
                trigger_emergency(voice)
                continue

            # --- SWITCHER ---
            if any(word in voice for word in ["arabic", "dubai"]): 
                CURRENT_MODE = "ar"; speak_feedback("Dubai Mode."); continue
            if any(word in voice for word in ["swahili", "kenya"]): 
                CURRENT_MODE = "sw"; speak_feedback("Kenya Mode."); continue

            if "exit" in voice or "stop" in voice:
                speak_feedback("Kwaheri."); break

            # --- TRANSLATION ---
            translation = ""
            words = voice.split()
            found_match = False
            for word in words:
                if word in ACTIVE_DICT:
                    translation = ACTIVE_DICT[word]; found_match = True; break
            
            if not found_match:
                matches = get_close_matches(voice, ACTIVE_DICT.keys(), n=1, cutoff=0.6)
                if matches: translation = ACTIVE_DICT[matches[0]]
                else: translation = "Unknown."

            print(f"Result: {translation}")
            if translation != "Unknown.": speak_feedback(translation)
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\n[!] Exit."); sys.exit()

if __name__ == "__main__":
    main()
