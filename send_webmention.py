import mailbox
from pip import main
import requests
import feedparser

feed_url = "http://fundor333.com/index.xml"


def send_webmention(url: str):
    params = {"url": url}
    # send post request to webmention
    r = requests.post(
        f"https://webmention.app/check?token=d6ecd337-f1c5-4b3f-8e82-5dc280d727fa&url={url}"
    )
    print(r.status_code)


def get_url_from_feed():
    for link in feedparser.parse(feed_url).entries:
        send_webmention(link.link)


if __name__ == '__main__':
    get_url_from_feed()
