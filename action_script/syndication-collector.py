import feedparser
from pathlib import Path
import os
import json
import hashlib
import requests
import re
import logging

domain = "https://fundor333.com"
rss = [
    "https://mastodon.social/@fundor333.rss",
    "https://bsky.app/profile/did:plc:u7piwonv4s27ysugjaa6im2q/rss",
    "https://fundor333.medium.com/feed",
]
hacker_news_username = "fundor333"


def clean_slug(slug: str):
    return hashlib.md5(
        (slug.split("?")[0]).encode("utf-8"), usedforsecurity=False
    ).hexdigest()


class HackerNewsFinder:
    def __init__(self, hacker_news_username):
        self.hacker_news_username = hacker_news_username
        self.path_folder = os.path.join("data", "syndication", "hacker_news")
        Path(self.path_folder).mkdir(parents=True, exist_ok=True)
        self.path_file = os.path.join(self.path_folder, self.hacker_news_username)
        if os.path.exists(self.path_file + ".json") is False:
            with open(self.path_file + ".json", "w") as fp:
                json.dump({"readed": []}, fp)

    def get_articles_id(self):
        url = f"https://hacker-news.firebaseio.com/v0/user/{self.hacker_news_username}.json"
        data = requests.get(url).json()
        return data.get("submitted", [])

    def get_article(self, article_id):
        url = f"https://hacker-news.firebaseio.com/v0/item/{article_id}.json"
        data = requests.get(url).json()
        if data.get("type", False) == "story":
            return (f"https://news.ycombinator.com/item?id={article_id}", data["url"])
        return False

    def run(self, output: dict):
        with open(self.path_file + ".json") as fp:
            data = json.load(fp)
            for link in self.get_articles_id():
                if link not in data["readed"]:
                    info = self.get_article(link)
                    if info:
                        hashed = clean_slug(info[1])
                        if output.get(hashed, False):
                            output[hashed].append(info[0])
                        else:
                            output[hashed] = [info[0]]
                    data["readed"].append(link)
        with open(self.path_file + ".json", "w") as fp:
            json.dump(data, fp)


class FeedFinder:
    def find_urls(self, string):
        urls = re.findall(r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+", string)

        return urls

    def get_label(self, feed_type: str, entry: dict):
        if feed_type == "rss20":
            return entry.get("summary")

        else:
            logging.error(f"Feed type not supported: {feed_type}")

            return entry.get("content")

    def run(self, rss_url: str, domain: str, output: dict):
        feed = feedparser.parse(rss_url)

        if feed.status == 200:
            for entry in feed.entries:
                link = entry.get("link")

                for e in self.find_urls(self.get_label(feed.version, entry)):
                    if domain in e:
                        e = clean_slug(e)
                        if output.get(e, False):
                            output[e].append(link.strip())
                        else:
                            output[e] = [link.strip()]
        else:
            logging.error("Failed to get RSS feed. Status code:", feed.status)


class WriterSyndication:
    def __init__(
        self,
        rss: list[str],
        hacker_news_username: str,
        domain: str,
    ):
        self.output = {}
        self.rss = rss
        self.domain = domain
        self.hacker_news_username = hacker_news_username

    def data_gathering(self):
        ff = FeedFinder()
        for i in self.rss:
            ff.run(i, self.domain, self.output)

        hn = HackerNewsFinder(self.hacker_news_username)
        hn.run(self.output)

    def write(self):
        for key in self.output.keys():

            path_folder = os.path.join("data", "syndication")

            Path(path_folder).mkdir(parents=True, exist_ok=True)
            path_file = os.path.join(path_folder, key)

            if os.path.exists(path_file + ".json"):
                with open(path_file + ".json") as fp:
                    data = json.load(fp)
                    if data.get("syndication", False):
                        data["syndication"] = sorted(
                            set(data["syndication"] + self.output[key])
                        )

                    else:
                        data["syndication"] = sorted(self.output[key])

            else:
                data = {"syndication": sorted(self.output[key])}

            with open(path_file + ".json", "w") as fp:
                json.dump(data, fp)

    def run(self):
        self.data_gathering()
        self.write()


w = WriterSyndication(
    rss,
    hacker_news_username,
    domain,
)
w.run()
