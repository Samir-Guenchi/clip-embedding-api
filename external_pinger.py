"""
External Keep-Alive Pinger for Hugging Face Space
Deploy this on Railway, Render, or run locally/on a VPS

This pings your HF Space every 25 minutes to prevent sleep
"""

import os
import time
import requests
from datetime import datetime
import schedule

SPACE_URL = os.getenv("HF_SPACE_URL", "https://huggingface.co/spaces/YOUR_USERNAME/alg")
PING_INTERVAL = 25  # minutes

def ping_space():
    """Send a ping to the Space"""
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pinging {SPACE_URL}...")
        response = requests.get(SPACE_URL, timeout=30)
        if response.status_code == 200:
            print(f"✅ Ping successful (200 OK)")
        else:
            print(f"⚠️ Ping returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Ping failed: {e}")

def main():
    print(f"🚀 HF Space Keep-Alive Pinger Started")
    print(f"📍 Target: {SPACE_URL}")
    print(f"⏰ Interval: Every {PING_INTERVAL} minutes")
    print("-" * 60)
    
    # Initial ping
    ping_space()
    
    # Schedule recurring pings
    schedule.every(PING_INTERVAL).minutes.do(ping_space)
    
    # Run forever
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
