#!/usr/bin/env python3
import getpass
import os
# Using getpass hides the characters as you type

'''password = getpass.getpass("Enter Riakoine Access Key: ")

if password == "700":
    print("\033[1;32mAccess Granted: Welcome, Rafiki.\033[0m")
else:
    print("\033[1;31mAccess Denied! Alerting Security...\033[0m")'''



#!/usr/bin/env python3


while True:
    password = getpass.getpass("Enter Access Key: ")
    
    if password == "700":
        print("Access Granted.")
        break  # This exits the loop and lets you in
    else:
        # This clears the screen and asks again
        os.system('clear')
        print("Incorrect. Try again.")

