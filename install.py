from db import DB

print("Welcome to the ODTU Telegram Bot Installer!")
try:
    db = DB()
    secret = input('Enter your Telegram Bot Secret: ')
    db.create_db(secret)
    print("Installation has been completed.\n")
except:
    print(
        "Installation failed. Please check if you have the necessary file permissions."
    )
