import feedparser
from datetime import datetime, timedelta
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# Liste der RSS-Feed-URLs
feed_urls = [
    "https://www.bfdi.bund.de/SiteGlobals/Functions/RSSFeed/Allgemein/rssnewsfeed.xml?nn=304054",
    "https://www.cpomagazine.com/feed/",
    "https://edpb.europa.eu/feed/news_en",
    "https://www.heise.de/thema/Datenschutz.xml",
    "https://iabeurope.eu/feed/",
    "https://iapp.org/rss/daily-dashboard",
    "https://www.baden-wuerttemberg.datenschutz.de/category/datenschutz/feed/"
]

def fetch_rss_feeds(include_yesterday: bool = False):
    articles = []
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)

    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published = datetime(*entry.published_parsed[:6]).date()
            
            if published == today or (include_yesterday and published == yesterday):
                # Abrufen von Titel, Link und Snippet
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': published.isoformat(),
                    'snippet': entry.summary if 'summary' in entry else 'Keine Zusammenfassung verfügbar'
                }
                articles.append(article)
    return articles

@app.get("/rss")
def read_rss(include_yesterday: Optional[bool] = False):
    articles = fetch_rss_feeds(include_yesterday)
    return {"articles": articles}
