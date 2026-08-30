import os
import feedparser
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

RSS_URL = "https://www.ynet.co.il/Integration/StoryRss1854.xml"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def main():
    feed = feedparser.parse(RSS_URL)
    if feed.entries:
        latest = feed.entries[0]
        title = latest.title
        link = latest.link
        
        message = f"<b>{title}</b>\n\n{link}"
        send_telegram_message(message)

if __name__ == "__main__":
    main()
