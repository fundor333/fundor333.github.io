import logging
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from syndication_cli.models import SyndicationConfig
from syndication_cli.utils import find_post_from_source

from .common import add_syndication_to_post, save_syndication_cache

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
MAX_RETRIES = 4
FEED_DELAY = 5


def _fetch_feed(url: str) -> str | None:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

        if resp.status_code == 429 and attempt < MAX_RETRIES:
            wait = float(resp.headers.get("x-ratelimit-reset") or 5) + attempt
            logger.warning(f"Rate limited by Reddit, retrying in {wait:.0f}s ({attempt}/{MAX_RETRIES})")
            time.sleep(wait)
            continue

        if not resp.ok or not resp.text:
            logger.error(f"Failed to fetch {url}: status {resp.status_code}")
            return None

        return resp.text

    return None


def process(config: SyndicationConfig) -> list[dict]:
    reddit_username = config.feeds.reddit
    if not reddit_username:
        return []

    logger.info(">> Processing Reddit")

    updates = []
    domain = config.site.domain
    content_dir = config.site.content_dir
    syndication_dir = config.paths.syndication_dir

    # The profile feed can silently miss posts, while the domain feed only has link posts:
    # read both and dedupe by entry id.
    reddit_domain = config.feeds.reddit_domain or urlparse(domain).netloc or domain
    feed_urls = [
        f"https://www.reddit.com/user/{reddit_username}/submitted.rss",
        f"https://www.reddit.com/domain/{reddit_domain}/new/.rss",
    ]

    entries = {}
    for i, feed_url in enumerate(feed_urls):
        if i:
            time.sleep(FEED_DELAY)
        logger.debug(f"Processing Reddit feed: {feed_url}")
        feed_text = _fetch_feed(feed_url)
        if not feed_text:
            continue
        for entry in BeautifulSoup(feed_text, "xml").find_all("entry"):
            author = entry.find("author")
            author_name = author.find("name") if author else None
            if not author_name or author_name.text.strip().removeprefix("/u/").lower() != reddit_username.lower():
                continue
            entry_id = entry.find("id")
            entries.setdefault(entry_id.text.strip() if entry_id else id(entry), entry)

    for entry in entries.values():
        link_elem = entry.find("link")
        if not link_elem or not link_elem.get("href"):
            continue
        reddit_link = str(link_elem["href"]).strip()

        content_elem = entry.find("content")
        content_html = content_elem.text if content_elem is not None and content_elem.text else ""

        soup_content = BeautifulSoup(content_html, "html.parser")
        source_links = [a["href"] for a in soup_content.find_all("a", href=True) if domain in a["href"]]

        if not source_links:
            continue

        source_url = str(source_links[0])

        if not config.options.dry_run:
            save_syndication_cache(source_url, [reddit_link], syndication_dir)

        post_path = find_post_from_source(source_url, content_dir)
        if not post_path:
            logger.debug(f"Post not found for source: {source_url}")
            continue

        added = add_syndication_to_post(post_path, [reddit_link], config.options.dry_run)
        if added:
            logger.info(f"Updated {post_path} from reddit")
            updates.append(
                {
                    "file": post_path,
                    "source": source_url,
                    "syndication": " | ".join(added),
                    "feed": "reddit",
                }
            )

    return updates
