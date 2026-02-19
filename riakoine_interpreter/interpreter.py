#!/usr/bin/env python3
from googletrans import Translator
from gtts import gTTS
import os
import time

# --- 1. SETUP THE BRAIN ---
translator = Translator()

def speak(text, lang_code):
    """Makes the phone speak using Google TTS"""
    try:
        # Create the audio file
        tts = gTTS(text=text, lang=lang_code, slow=False)
        filename = "voice_temp.mp3"
        tts.save(filename)
        
        # Play audio silently (hides the video popup)
        # We use '--vo=null' to disable video and '> /dev/null' to hide text
        os.system(f"mpv {filename} --vo=null > /dev/null 2>&1")
        
        # Clean up
        os.remove(filename)
    except Exception as e:
        print(f"⚠️ Audio Error: {e}")

def chat_mode():
    os.system('clear')
    print("=======================================")
    print("    🌍 RIAKOINE GLOBAL LINK 🌍")
    print("=======================================")
    print("  1. 🇦🇪 Dubai Mode (English <-> Arabic)")
    print("  2. 🇰🇪 Home Mode  (English <-> Swahili)")
    print("  3. 🇨🇦 Tech Mode  (English <-> French)")
    print("=======================================")
    
    choice = input("\nSelect Channel (1-3): ")

    if choice == '1':
        target_lang = 'ar'
        target_name = "Arabic"
    elif choice == '2':
        target_lang = 'sw'
        target_name = "Swahili"
    elif choice == '3':
        target_lang = 'fr'
        target_name = "French"
    else:
        print("Invalid choice. Exiting.")
        return

    print(f"\n✅ Connected: English <-> {target_name}")
    print("(Type 'exit' to quit)\n")

    while True:
        # --- PART A: YOU SPEAK (English) ---
        print(f"\n[ 👤 YOU (English) ]")
        my_text = input(">> ")
        
        if my_text.lower() == 'exit': break

        try:
            # Translate English -> Target
            translated = translator.translate(my_text, dest=target_lang)
            print(f"   🔊 {target_name}: {translated.text}")
            
            # Phone Speaks to Listener
            speak(translated.text, target_lang)
        except Exception as e:
            print("Translation Error. Check Internet.")

        # --- PART B: THEY SPEAK (Target Language) ---
        print(f"\n[ 👥 LISTENER ({target_name}) ]")
        their_text = input(">> ")

        if their_text.lower() == 'exit': break

        try:
            # Translate Target -> English
            back_home = translator.translate(their_text, dest='en')
            print(f"   🔊 English: {back_home.text}")
            
            # Phone Speaks to You
            speak(back_home.text, 'en')
        except Exception as e:
            print("Translation Error.")

if __name__ == "__main__":
    chat_mode()
