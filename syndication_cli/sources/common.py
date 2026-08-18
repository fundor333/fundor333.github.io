import logging
import re
import warnings
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

from syndication_cli.models import SyndicationConfig
from syndication_cli.utils import find_post_from_source, normalize_url, parse_fediverse_url

logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)


def add_syndication_to_post(filepath: str, new_links: list[str], dry_run: bool = False) -> list[str]:
    with Path(filepath).open(encoding="utf-8") as f:
        content = f.read()

    if content.startswith("++"):
        raise NotImplementedError("TOML frontmatter not supported")

    if not content.startswith("---"):
        logger.error(f"Unknown frontmatter format: {filepath}")
        return []

    match = re.match(r"^---\n(.+?)\n---", content, re.DOTALL)
    if not match:
        logger.error(f"Invalid frontmatter in {filepath}")
        return []

    frontmatter_raw = match.group(1)
    body = content[match.end() :]

    body = "\n" + body.lstrip("\n")

    frontmatter = yaml.safe_load(frontmatter_raw)
    existing = frontmatter.get("syndication", [])

    if isinstance(existing, str):
        existing = [existing] if existing else []
    elif existing is None:
        existing = []

    existing_norm = set(map(normalize_url, existing))
    new_norm = set(map(normalize_url, new_links))
    to_add = list(new_norm - existing_norm)

    if not to_add:
        return []

    frontmatter["syndication"] = sorted(existing_norm.union(new_norm))

    for link in to_add:
        parsed = parse_fediverse_url(link)
        if parsed:
            frontmatter["comments"] = parsed

    if not dry_run:
        new_frontmatter = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True)
        new_content = f"---\n{new_frontmatter}---\n{body}"
        new_content = new_content.replace(": null", ":")
        with Path(filepath).open("w", encoding="utf-8") as f:
            f.write(new_content)

    logger.info(f"Added {len(to_add)} syndication links to {filepath}")
    return to_add


def process_rss_feed(feed_url: str, feed_name: str, config: SyndicationConfig) -> list[dict]:
    updates = []
    domain = config.site.domain
    content_dir = config.site.content_dir

    logger.debug(f"Processing {feed_name} feed: {feed_url}")
    resp = requests.get(feed_url, timeout=10)
    soup = BeautifulSoup(resp.text, "xml")

    for item in soup.find_all("item"):
        guid_elem = item.find("guid")
        if not guid_elem or not guid_elem.text:
            continue
        guid = guid_elem.text.strip()

        desc_elem = item.find("description")
        content_html = desc_elem.text if desc_elem is not None and desc_elem.text else ""

        soup_descr = BeautifulSoup(content_html, "html.parser")
        source_links = [a["href"] for a in soup_descr.find_all("a", href=True) if domain in a["href"]]

        if not source_links:
            continue

        source_url = source_links[0]
        post_path = find_post_from_source(source_url, content_dir)
        if not post_path:
            logger.debug(f"Post not found for source: {source_url}")
            continue

        added = add_syndication_to_post(post_path, [guid], config.options.dry_run)
        if added:
            logger.info(f"Updated {post_path} from {feed_name}")
            updates.append(
                {
                    "file": post_path,
                    "source": source_url,
                    "syndication": " | ".join(added),
                    "feed": feed_name,
                }
            )

    return updates
