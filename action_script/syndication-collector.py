import feedparser
from pathlib import Path
import os
import json
import hashlib

domain = "https://fundor333.com"
rss_url_mastodon = "https://mastodon.social/@fundor333.rss"
rss_url_bsky = "https://bsky.app/profile/did:plc:u7piwonv4s27ysugjaa6im2q/rss"


def clean_slug(slug: str):
    return hashlib.md5(
        (slug.split("?")[0]).encode("utf-8"), usedforsecurity=False
    ).hexdigest()


class BskyFinder:
    def find_urls(self, string):
        x = string.split(" ")
        res = []
        for i in x:
            if i.startswith("https:") or i.startswith("http:"):
                res.append(i)
        return res

    def run(self, rss_url: str, domain: str, output: dict):
        feed = feedparser.parse(rss_url)
        if feed.status == 200:
            for entry in feed.entries:
                link = entry.get("link")
                for e in self.find_urls(entry.get("summary")):
                    if domain in e:
                        e = clean_slug(e)
                        if output.get(e, False):
                            output[e].append(link.strip())
                        else:
                            output[e] = [link.strip()]
        else:
            print("Failed to get RSS feed. Status code:", feed.status)


class MastodonFinder:
    def find_urls(self, string):
        x = string.split('"')
        res = []
        for i in x:
            if i.startswith("https:") or i.startswith("http:"):
                res.append(i)
        return res

    def run(self, rss_url: str, domain: str, output: dict):
        feed = feedparser.parse(rss_url)
        if feed.status == 200:
            for entry in feed.entries:
                link = entry.get("link")
                for e in self.find_urls(entry.get("description")):
                    if domain in e:
                        e = clean_slug(e)
                        if output.get(e, False):
                            output[e].append(link.strip())
                        else:
                            output[e] = [link.strip()]
        else:
            print("Failed to get RSS feed. Status code:", feed.status)


class WriterSyndication:
    def __init__(self, rss_url_mastodon: str, rss_url_bsky: str, domain: str):
        self.output = {}
        self.rss_url_mastodon = rss_url_mastodon
        self.rss_url_bsky = rss_url_bsky
        self.domain = domain

    def data_gathering(self):
        m = MastodonFinder()
        m.run(self.rss_url_mastodon, self.domain, self.output)

        bs = BskyFinder()
        bs.run(self.rss_url_bsky, self.domain, self.output)

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


w = WriterSyndication(rss_url_mastodon, rss_url_bsky, domain)
w.run()
