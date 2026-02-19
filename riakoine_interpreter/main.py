import os
import subprocess
import json
import requests
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from dotenv import load_dotenv
from difflib import get_close_matches

load_dotenv()
EMERGENCY_CONTACT = os.getenv("EMERGENCY_CONTACT")
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

GLOBAL_SOS_KEYWORDS = ["help", "emergency", "tawari", "tulong", "saidia", "danger", "sos", "police", "shorta", "pulis"]

class RiakoineApp(App):
    def build(self):
        self.current_mode = "sw"
        self.last_alert_time = 0  # Cooldown tracker
        Window.clearcolor = (0.05, 0.1, 0.15, 1)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        self.status_label = Label(text="RIAKOINE GLOBAL SHIELD", font_size='24sp', bold=True, size_hint_y=0.2)
        self.layout.add_widget(self.status_label)
        
        self.mode_label = Label(text="Mode: KENYA (Swahili)", font_size='18sp', color=(0, 1, 0.5, 1), size_hint_y=0.1)
        self.layout.add_widget(self.mode_label)

        self.result_label = Label(text="Global Protection Active", font_size='20sp', italic=True)
        self.layout.add_widget(self.result_label)
        
        self.mic_btn = Button(text="🎤 SPEAK ANY LANGUAGE", background_color=(0, 0.4, 0.8, 1), font_size='20sp', bold=True)
        self.mic_btn.bind(on_press=self.start_listening)
        self.layout.add_widget(self.mic_btn)
        
        self.sos_btn = Button(text="🚨 GLOBAL SOS 🚨", background_color=(0.8, 0, 0, 1), font_size='22sp', bold=True, size_hint_y=0.3)
        self.sos_btn.bind(on_press=self.trigger_sos_manual)
        self.layout.add_widget(self.sos_btn)

        return self.layout

    def start_listening(self, instance):
        self.result_label.text = "Listening..."
        Clock.schedule_once(self.process_voice, 0.1)

    def process_voice(self, dt):
        voice = subprocess.getoutput("termux-speech-to-text").strip().lower()
        if not voice:
            self.result_label.text = "No audio detected."
            return

        if any(word in voice for word in GLOBAL_SOS_KEYWORDS):
            self.trigger_emergency(f"GLOBAL TRIGGER: {voice}")
            return

        # Simple Language Switcher
        if any(w in voice for w in ["dubai", "arabic"]): self.current_mode = "ar"; self.mode_label.text = "Mode: DUBAI"; return
        elif any(w in voice for w in ["kenya", "swahili"]): self.current_mode = "sw"; self.mode_label.text = "Mode: KENYA"; return

        self.result_label.text = f"Heard: {voice}"
        os.system(f"termux-tts-speak 'Received'")

    def trigger_sos_manual(self, instance):
        self.trigger_emergency("MANUAL BUTTON PRESS")

    def trigger_emergency(self, reason):
        current_time = time.time()
        
        # --- 🕒 60 SECOND COOLDOWN ---
        if current_time - self.last_alert_time < 60:
            print("Alert skipped: Cooldown active.")
            os.system("termux-vibrate -d 200")
            self.result_label.text = "Alert already sent. Standing by."
            return

        self.last_alert_time = current_time
        os.system("termux-vibrate -d 2000")
        self.result_label.text = "🚨 BROADCASTING ALERTS 🚨"
        
        if TG_TOKEN and TG_CHAT_ID:
            try:
                msg = f"🌍 *GLOBAL SOS*\nReason: {reason}\nContact: {EMERGENCY_CONTACT}"
                requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                              data={"chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, 
                              timeout=5)
            except: pass

        os.system(f'termux-sms-send -n {EMERGENCY_CONTACT} "RIAKOINE SOS: {reason}"')
        os.system("termux-tts-speak 'Alert broadcasted.'")

if __name__ == '__main__':
    RiakoineApp().run()
