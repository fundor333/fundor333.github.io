import logging

import requests
from bs4 import BeautifulSoup

from syndication_cli.models import SyndicationConfig
from syndication_cli.utils import find_post_from_source

from .common import add_syndication_to_post, save_syndication_cache

logger = logging.getLogger(__name__)


def process(config: SyndicationConfig) -> list[dict]:
    feed_url = config.feeds.medium
    if not feed_url:
        return []

    logger.info(">> Processing Medium")

    updates = []
    domain = config.site.domain
    content_dir = config.site.content_dir

    logger.debug(f"Processing Medium feed: {feed_url}")
    resp = requests.get(feed_url, timeout=10)
    soup = BeautifulSoup(resp.content, "xml")

    for item in soup.find_all("item"):
        link_elem = item.find("link")
        if not link_elem or not link_elem.text:
            continue
        link_medium = link_elem.text.strip()

        encoded = item.find("content:encoded")
        desc_elem = item.find("description")
        content_html = (
            encoded.text
            if encoded is not None and encoded.text
            else (desc_elem.text if desc_elem is not None and desc_elem.text else "")
        )

        soup_descr = BeautifulSoup(content_html, "html.parser")
        source_links = [a["href"] for a in soup_descr.find_all("a", href=True) if domain in a["href"]]

        if not source_links:
            continue

        source_url = source_links[0]

        if not config.options.dry_run:
            save_syndication_cache(source_url, [link_medium], config.paths.syndication_dir)

        post_path = find_post_from_source(source_url, content_dir)
        if not post_path:
            logger.debug(f"Post not found for source: {source_url}")
            continue

        added = add_syndication_to_post(post_path, [link_medium], config.options.dry_run)
        if added:
            logger.info(f"Updated {post_path} from medium")
            updates.append(
                {
                    "file": post_path,
                    "source": source_url,
                    "syndication": " | ".join(added),
                    "feed": "medium",
                }
            )

    return updates
