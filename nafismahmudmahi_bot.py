import feedparser
import time
import requests

# === CONFIG ===
CHANNEL_ID = 'UCeMsqI6jU9WE2ctsrbxbywQ'
RSS_FEED = f'https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}'
BOT_TOKEN = 'YOUR_BOT_TOKEN'     # Replace with your Telegram bot token
CHAT_ID = 'YOUR_CHAT_ID'         # Replace with your own Telegram user ID or group ID

# To keep track of last notified video
last_video_id = None

def get_latest_video():
    feed = feedparser.parse(RSS_FEED)
    if feed.entries:
        latest = feed.entries[0]
        return latest.id, latest.title, latest.link
    return None, None, None

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)

# === Main loop ===
while True:
    try:
        video_id, title, link = get_latest_video()
        if video_id and video_id != last_video_id:
            last_video_id = video_id
            message = f"🎥 *New YouTube Video Uploaded!*\n\n📌 *{title}*\n🔗 [Watch Now]({link})"
            send_telegram_message(message)
            print(f"✅ Notified: {title}")
    except Exception as e:
        print("❌ Error:", e)

    time.sleep(300)  # check every 5 minutes
