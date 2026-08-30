import os
import json
import feedparser
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

RSS_URLS = [
    "https://mako.co.il/rss/news-mako-news.xml",
    "https://www.israelhayom.co.il/rss.xml",
    "https://www.ynet.co.il/Integration/StoryRss1854.xml"
]

SENT_ARTICLES_FILE = "sent_articles.json"

def load_sent_articles():
    if os.path.exists(SENT_ARTICLES_FILE):
        try:
            with open(SENT_ARTICLES_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception as e:
            print("Error loading sent articles:", e)
    return set()

def save_sent_articles(sent_articles):
    with open(SENT_ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(list(sent_articles), f, ensure_ascii=False)

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    response = requests.post(url, json=payload)
    print("Telegram Response Status:", response.status_code)
    print("Telegram Response Body:", response.text)

def main():
    sent_articles = load_sent_articles()
    new_sent_count = 0

    for url in RSS_URLS:
        feed = feedparser.parse(url)
        if feed.entries:
            # בודקים את הכתבות האחרונות בפיד
            for entry in reversed(feed.entries[:5]):
                article_id = entry.get("id") or entry.get("link")
                if article_id not in sent_articles:
                    title = entry.title
                    link = entry.link
                    
                    message = f"<b>{title}</b>\n\n{link}"
                    send_telegram_message(message)
                    
                    sent_articles.add(article_id)
                    new_sent_count += 1

    # שמירת הרשימה כדי שלא יישלחו שוב בריצה הבאה
    save_sent_articles(sent_articles)
    print(f"Finished. Sent {new_sent_count} new articles.")

if __name__ == "__main__":
    main()
