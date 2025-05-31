import feedparser
import requests
import os

# === CONFIG ===
CHANNEL_ID = 'UCeMsqI6jU9WE2ctsrbxbywQ'
RSS_FEED = f'https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}'
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
STATE_FILE = "last_video.txt"

def get_latest_video():
    feed = feedparser.parse(RSS_FEED)
    if feed.entries:
        latest = feed.entries[0]
        return latest.id, latest.title, latest.link
    return None, None, None

def read_last_video_id():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return f.read().strip()
    return None

def write_last_video_id(video_id):
    with open(STATE_FILE, 'w') as f:
        f.write(video_id)

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)

# === MAIN LOGIC ===
last_video_id = read_last_video_id()
video_id, title, link = get_latest_video()

if video_id and video_id != last_video_id:
    write_last_video_id(video_id)
    send_telegram_message(f"🎥 *New Video Uploaded!*\n\n📌 *{title}*\n🔗 [Watch Now]({link})")
    print("✅ Notification sent.")
else:
    print("No new video.")
