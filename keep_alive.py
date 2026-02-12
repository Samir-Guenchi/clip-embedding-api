"""
Keep-Alive service for Hugging Face Spaces
Runs a background thread that pings itself every 30 minutes to prevent sleep
"""

import threading
import time
import requests
from datetime import datetime

class KeepAlive:
    def __init__(self, space_url: str, interval: int = 1800):
        """
        Args:
            space_url: Your HF Space URL (e.g., 'https://huggingface.co/spaces/USERNAME/SPACENAME')
            interval: Ping interval in seconds (default 1800 = 30 minutes)
        """
        self.space_url = space_url
        self.interval = interval
        self.running = False
        self.thread = None
    
    def _ping(self):
        """Send a lightweight ping to the Space"""
        while self.running:
            try:
                response = requests.get(self.space_url, timeout=10)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Keep-alive ping: {response.status_code}")
            except Exception as e:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Keep-alive ping failed: {e}")
            
            time.sleep(self.interval)
    
    def start(self):
        """Start the keep-alive service"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._ping, daemon=True)
            self.thread.start()
            print(f"Keep-alive service started (ping every {self.interval}s)")
    
    def stop(self):
        """Stop the keep-alive service"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("Keep-alive service stopped")
