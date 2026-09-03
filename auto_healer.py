import time
import requests
import subprocess

# Provide your Telegram Bot credentials here
BOT_TOKEN = "8324196647:AAFvy0KPkC4YSjRJgLWFcx_VZ1QldNQWSJE"
CHAT_ID = "1202275253"
SITE_URL = "http://127.0.0.1:80"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

print("🛡️ AIOps Auto-Healer is monitoring the Tech Store...")

while True:
    try:
        # Check if the website is running and responsive
        response = requests.get(SITE_URL)
        if response.status_code != 200:
            raise Exception("Site is down!")
    except Exception as e:
        print("❌ Crash Detected! Initiating Auto-Healing...")
        send_telegram_alert("🚨 AIOps Alert: E-commerce site is DOWN! Auto-healing initiated...")
        
        # Command to restart the website in the background
        subprocess.Popen(["sudo", "python3", "app.py"])
        
        send_telegram_alert("✅ AIOps Recovery: Site successfully restarted!")
        time.sleep(10) # Allow time for the server to restart
    
    time.sleep(5) # Check health every 5 seconds