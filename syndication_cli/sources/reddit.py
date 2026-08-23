import logging

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from syndication_cli.models import SyndicationConfig
from syndication_cli.utils import find_post_from_source

from .common import add_syndication_to_post, save_syndication_cache

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)


def _fetch_via_browser(url: str) -> str | None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_context(user_agent=USER_AGENT).new_page()
            response = page.goto(url, wait_until="domcontentloaded", timeout=15000)
            logger.info(f"Fetched {url} via browser: status {response.status if response else 'unknown'}")
            if response is None or not response.ok:
                status = response.status if response else "unknown"
                logger.error(f"Failed to fetch {url} via browser: status {status}")
                return None
            return response.text()
        finally:
            browser.close()


def process(config: SyndicationConfig) -> list[dict]:
    reddit_username = config.feeds.reddit
    if not reddit_username:
        return []

    logger.info(">> Processing Reddit")

    updates = []
    domain = config.site.domain
    content_dir = config.site.content_dir
    syndication_dir = config.paths.syndication_dir

    feed_url = f"https://www.reddit.com/user/{reddit_username}.rss"
    logger.debug(f"Processing Reddit feed via browser: {feed_url}")

    feed_text = _fetch_via_browser(feed_url)
    if not feed_text:
        return updates

    soup = BeautifulSoup(feed_text, "xml")

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
