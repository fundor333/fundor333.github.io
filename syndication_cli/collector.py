import json
import logging
from pathlib import Path

import feedparser
import requests

from .models import SyndicationConfig
from .utils import clean_slug, ensure_directory, find_urls

logger = logging.getLogger(__name__)


class HackerNewsFinder:
    def __init__(self, username: str, output: dict, syndication_dir: str):
        self.username = username
        self.output = output
        self.hn_dir = Path(syndication_dir) / "hacker_news"
        ensure_directory(str(self.hn_dir))
        self.hn_file = self.hn_dir / f"{username}.json"
        if not self.hn_file.exists():
            self._save_readed([])

    def _load_readed(self) -> list:
        with self.hn_file.open(encoding="utf-8") as f:
            return json.load(f).get("readed", [])

    def _save_readed(self, readed: list) -> None:
        with self.hn_file.open("w", encoding="utf-8") as f:
            json.dump({"readed": readed}, f)

    def _get_articles(self) -> list:
        page = 0
        all_articles = []
        base_url = "https://hn.algolia.com/api/v1/search"

        while True:
            url = f"{base_url}?tags=author_{self.username}&hitsPerPage=100&page={page}"
            response = requests.get(url, timeout=10).json()
            hits = response.get("hits", [])
            if not hits:
                break
            all_articles.extend(hits)
            if page >= response.get("nbPages", 1) - 1:
                break
            page += 1

        return all_articles

    def _get_article_info(self, article: dict) -> tuple | None:
        if "story" not in article.get("_tags", []):
            return None
        if article.get("dead", False):
            return None
        url = article.get("url")
        if not url:
            return None
        hn_link = f"https://news.ycombinator.com/item?id={article.get('objectID')}"
        return (hn_link, url)

    def run(self) -> None:
        readed = self._load_readed()
        for article in self._get_articles():
            article_id = article.get("objectID")
            if article_id in readed:
                continue

            info = self._get_article_info(article)
            if info:
                hashed = clean_slug(info[1])
                if self.output.get(hashed):
                    self.output[hashed].append(info[0])
                else:
                    self.output[hashed] = [info[0]]

            readed.append(article_id)

        self._save_readed(sorted(set(readed)))
        logger.info(f"HackerNews: processed {len(readed)} articles")


class FeedFinder:
    def _get_label(self, feed_version: str, entry: dict) -> str | None:
        if feed_version == "rss20":
            return entry.get("summary")
        return entry.get("content")

    def run(self, rss_url: str, domain: str, output: dict, data: dict) -> None:
        logger.debug(f"Fetching feed: {rss_url}")
        feed = feedparser.parse(rss_url)

        if feed.status != 200:
            logger.error(f"Failed to fetch {rss_url}: status {feed.status}")
            return

        for entry in feed.entries:
            link = entry.get("link")
            label = self._get_label(feed.version, entry)
            if not label:
                continue

            for url in find_urls(label):
                if domain not in url:
                    continue

                hashed = clean_slug(url)
                data[hashed] = url

                if output.get(hashed):
                    output[hashed].append(link.strip() if link else "")
                else:
                    output[hashed] = [link.strip() if link else ""]


class IndieWebFinder:
    def _get_label(self, feed_version: str, entry: dict) -> str | None:
        if feed_version == "rss20":
            return entry.get("summary")
        if feed_version == "atom10":
            return entry.get("id")
        return entry.get("content")

    def run(self, feed_url: str, site_label: str, domain: str, output: dict, data: dict) -> None:
        logger.debug(f"Fetching IndieWeb feed: {feed_url}")
        feed = feedparser.parse(feed_url)

        if feed.status != 200:
            logger.error(f"Failed to fetch {feed_url}: status {feed.status}")
            return

        for entry in feed.entries:
            label = self._get_label(feed.version, entry)
            if not label:
                continue

            for url in find_urls(label):
                if domain not in url:
                    continue

                hashed = clean_slug(url)
                data[hashed] = url

                if output.get(hashed):
                    output[hashed].append(site_label)
                else:
                    output[hashed] = [site_label]


class Collector:
    def __init__(self, config: SyndicationConfig):
        self.config = config
        self.output: dict[str, list[str]] = {}
        self.data: dict[str, str] = {}

    def _collect_feeds(self) -> None:
        domain = self.config.site.domain

        feeds = self.config.feeds
        feed_finder = FeedFinder()

        for feed_url in [feeds.mastodon, feeds.bluesky, feeds.medium]:
            if feed_url:
                feed_finder.run(feed_url, domain, self.output, self.data)

        indieweb_finder = IndieWebFinder()
        for item in feeds.indieweb:
            if item.get("url") and item.get("site"):
                indieweb_finder.run(item["url"], item["site"], domain, self.output, self.data)

    def _collect_hacker_news(self) -> None:
        hn_config = self.config.external.hacker_news
        if not hn_config.enabled or not hn_config.username:
            logger.info("HackerNews collection disabled")
            return

        hn_finder = HackerNewsFinder(hn_config.username, self.output, self.config.paths.syndication_dir)
        hn_finder.run()

    def _write_json_files(self) -> None:
        syndication_dir = Path(self.config.paths.syndication_dir)
        ensure_directory(str(syndication_dir))

        for key in self.output:
            filepath = syndication_dir / f"{key}.json"

            if filepath.exists():
                with filepath.open(encoding="utf-8") as f:
                    data = json.load(f)
                data["source"] = self.data.get(key)
                if data.get("syndication"):
                    data["syndication"] = sorted(set(data["syndication"] + self.output[key]))
                else:
                    data["syndication"] = sorted(self.output[key])
            else:
                data = {"syndication": sorted(self.output[key])}

            with filepath.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Wrote {len(self.output)} JSON files")

    def run(self) -> None:
        logger.info("Starting collection...")
        self._collect_feeds()
        self._collect_hacker_news()
        self._write_json_files()
        logger.info("Collection completed")


def collect(config: SyndicationConfig) -> None:
    collector = Collector(config)
    collector.run()
