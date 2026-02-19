#!/usr/bin/env python3
import requests
import getpass

# 1. Secure Entry
key = getpass.getpass("Enter Riakoine Vault Key: ")

if key != "700":
    print("Intruder Alert! Access Logged.")
    exit()

print("\n--- WELCOME TO THE GLOBAL LEDGER ---")

# 2. Live Data Fetching
# We'll use a free API to get the pulse of Canada and Dubai
try:
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    data = requests.get(url).json()
    
    aed = data['rates']['AED']
    cad = data['rates']['CAD']
    kes = data['rates']['KES']

    print(f"📍 Dubai (AED): {aed} / USD")
    print(f"📍 Canada (CAD): {cad} / USD")
    print(f"📍 Kenya (KES): {kes} / USD")
    
    print("\n--- MARKET ANALYSIS ---")
    if cad < 1.30:
        print("🇨🇦 CAD is Strong: Good for Canadian exports!")
    else:
        print("🇨🇦 CAD is Weak: Good for Dubai investors buying in Canada.")

except Exception as e:
    print("Error connecting to Global Markets. Check your internet.")
