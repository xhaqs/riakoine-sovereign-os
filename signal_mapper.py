import requests
import time
from plyer import vibrator

# Imperial Signal Configuration
CHECK_INTERVAL = 20  # seconds
HOST_TO_PING = "https://www.google.com"

def signal_sentry_loop():
    print("📡 RI-OS: Signal Sentry is on the wall...")
    while True:
        try:
            # Check the bridge
            requests.get(HOST_TO_PING, timeout=5)
            # Signal is healthy - no vibration
        except:
            print("⚠️ SIGNAL LOST: Kiserian is dark.")
            try:
                # LONG PULSE: 2 seconds to distinguish from messages
                vibrator.vibrate(2) 
                # Note: On the phone, we will add a specific audio 'ping' here too
            except Exception as e:
                print(f"Hardware alert failed: {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    signal_sentry_loop()
