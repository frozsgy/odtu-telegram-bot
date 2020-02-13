from db import DB

import os

print("Welcome to the ODTU Telegram Bot Installer!")
try:
    l = DB()
    secret = input('Enter your Telegram Bot Secret: ')
    l.create_db(secret)
    print("Installation has been completed.\n")
except:
    print("Installation failed. Please check if you have the necessary file permissions.")



