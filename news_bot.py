import feedparser
import telebot
import time
import hashlib
from difflib import SequenceMatcher

# Telegram bot məlumatları
BOT_TOKEN = '8158133901:AAE-jkP2Pq0KVhR8KiIUYwtw0vR-E1brYw0'
CHAT_ID = '@echoreports'
bot = telebot.TeleBot(BOT_TOKEN)

print("✅ Bot işə düşdü və xəbərləri yoxlayır...")

# RSS mənbələri
RSS_FEEDS = {
    "BBC": "https://feeds.bbci.co.uk/news/rss.xml",
    "Reuters": "https://www.reutersagency.com/feed/?best-topics=top-news",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml"
}

# Göndərilmiş xəbərlərin hash-ları
sent_hashes = set()

# Oxşarlıq threshold-u
SIMILARITY_THRESHOLD = 0.6

# Hash generasiya funksiyası
def get_news_hash(title):
    return hashlib.md5(title.lower().encode()).hexdigest()

# Başlıq oxşarlığı funksiyası
def is_similar(title1, title2):
    return SequenceMatcher(None, title1.lower(), title2.lower()).ratio()>= SIMILARITY_THRESHOLD

# RSS feed-dən xəbərləri çəkən funksiya
def get_news_from_feed(source_name, url):
    print(f"🔍 {source_name} üçün xəbərlər yüklənir...")
    feed = feedparser.parse(url)
    print(f"📥 {source_name} üçün {len(feed.entries)} xəbər tapıldı.")
    news_items = []
    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        text = f"📡 {source_name}\n📰 {title}\n🔗 {link}"
        news_items.append({"title": title, "link": link, "text": text})
    return news_items

# Filtrasiya və göndərmə funksiyası
def send_filtered_news():
    all_news = []

    for source, url in RSS_FEEDS.items():
        news = get_news_from_feed(source, url)
        print(f"🧪 {source} feed-dən ilk başlıq: {news[0]['title'] if news else 'Yoxdur'}")
        all_news.extend(news)

    print(f"🔎 Ümumi {len(all_news)} xəbər toplandı. Filtrasiya başlayır...")

    for item in all_news:
        news_hash = get_news_hash(item['title'])

        # Əvvəl göndərilmişsə, keç
        if news_hash in sent_hashes:
            print(f"⛔ Təkrar xəbər: {item['title']}")
            continue

        # Oxşar başlıqlar varsa, keç
        if any(
            is_similar(item['title'], prev['title'])
            for prev in all_news
            if get_news_hash(prev['title']) in sent_hashes
):
            print(f"⚠️ Oxşar xəbər filtr edildi: {item['title']}")
            continue

        # Göndərilməyəcək, sadəcə konsola yazılacaq
        print(f"📤 Göndərilməli idi: {item['title']}")
        print(item['text'])  # Əlavə olaraq tam mətn konsola yazılır

        sent_hashes.add(news_hash)
        time.sleep(1)
