import logging

import requests
from bs4 import BeautifulSoup

from syndication_cli.models import SyndicationConfig
from syndication_cli.utils import find_post_from_source

from .common import add_syndication_to_post

logger = logging.getLogger(__name__)


def process(config: SyndicationConfig) -> list[dict]:
    reddit_username = config.feeds.reddit
    if not reddit_username:
        return []

    logger.info(">> Processing Reddit")

    updates = []
    domain = config.site.domain
    content_dir = config.site.content_dir

    feed_url = f"https://www.reddit.com/user/{reddit_username}.rss"
    logger.debug(f"Processing Reddit feed: {feed_url}")
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:153.0) Gecko/20100101 Firefox/153.0"}
    resp = requests.get(feed_url, headers=headers, timeout=10)
    if resp.status_code != 200:
        logger.error(f"Failed to fetch Reddit feed {feed_url}: status {resp.status_code}")
        return updates

    soup = BeautifulSoup(resp.text, "xml")

    for entry in soup.find_all("entry"):
        link_elem = entry.find("link")
        if not link_elem or not link_elem.get("href"):
            continue
        reddit_link = link_elem["href"].strip()

        content_elem = entry.find("content")
        content_html = content_elem.text if content_elem is not None and content_elem.text else ""

        soup_content = BeautifulSoup(content_html, "html.parser")
        source_links = [a["href"] for a in soup_content.find_all("a", href=True) if domain in a["href"]]

        if not source_links:
            continue

        source_url = source_links[0]
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
