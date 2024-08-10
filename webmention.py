import requests
import feedparser
from rich.console import Console
from rich.text import Text

feed_url = "http://fundor333.com/index.xml"


def get_webmention(url_post: str):
    url = "https://webmention.io/api/mentions.jf2"

    payload = {'target[]': url_post}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(url_post)
    print(response.json()['children'])


def get_url_from_feed():
    for link in feedparser.parse(feed_url).entries:
        get_webmention(link.link)


get_url_from_feed()
