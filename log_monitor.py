import time
import requests
import os

BOT_TOKEN = "8324196647:AAFvy0KPkC4YSjRJgLWFcx_VZ1QldNQWSJE"
CHAT_ID = "1202275253"
LOG_FILE = "auth.log"

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    except:
        pass

print("🕵️‍♂️ AIOps Security Monitor is watching auth.log for hackers...")

# Create the log file if it does not exist
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, 'a').close()

with open(LOG_FILE, "r") as file:
    # Move to the end of the file to read only new log entries
    file.seek(0, 2) 
    while True:
        line = file.readline()
        if not line:
            time.sleep(1)
            continue
        
        # Detect unauthorized activity and trigger an alert if a failed login is found
        if "FAILED LOGIN ATTEMPT" in line:
            print(f"🚨 ALERT: Hacker detected! \n{line.strip()}")
            send_telegram_alert(f"🚨 AIOps Security Alert!\nUnauthorized Access Attempt Detected.\nDetails: {line.strip()}")