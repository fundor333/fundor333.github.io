import requests
import feedparser
from rich.console import Console
from rich.text import Text

feed_url = [
    "http://fundor333.com/index.xml",
]


def send_webmention(url: str):
    # send post request to webmention
    r = requests.post(
        f"https://webmention.app/check?token=d6ecd337-f1c5-4b3f-8e82-5dc280d727fa&url={url}"
    )
    console = Console()
    if 200 <= r.status_code < 400:
        color = "green"
    else:
        color = "red"
    text = Text.assemble((str(r.status_code), color), f" {url}")
    console.print(text)


def get_url_from_feed(feed_url: str):
    for link in feedparser.parse(feed_url).entries:
        send_webmention(link.link)


if __name__ == "__main__":
    for url in feed_url:
        get_url_from_feed(url)
