import json
import logging
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from .models import SyndicationConfig

logger = logging.getLogger(__name__)


def _extract_domain_link_from_mastodon(mastodon_url: str, domain: str) -> str | None:
    match = re.search(r"/@[^/]+/(\d+)", mastodon_url)
    if not match:
        return None

    post_id = match.group(1)
    api_url = f"https://mastodon.social/api/v1/statuses/{post_id}"

    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code != 200:
            logger.warning(f"API returned status {response.status_code} for {mastodon_url}")
            return None
    except requests.RequestException as e:
        logger.error(f"Request failed for {mastodon_url}: {e}")
        return None

    status_data = response.json()
    content_html = status_data.get("content", "")

    soup = BeautifulSoup(content_html, "html.parser")
    links = soup.find_all("a", href=True)

    for link in links:
        href = link["href"]
        if domain in href:
            return href

    return None


def _correct_json_file(filepath: str, domain: str, dry_run: bool = False) -> bool:
    with Path(filepath).open(encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON: {filepath}")
            return False

    mastodon_url = None
    for url in data.get("syndication", []):
        if "mastodon.social" in url:
            mastodon_url = url
            break

    if not mastodon_url:
        logger.debug(f"No Mastodon URL in {filepath}")
        return False

    source_link = _extract_domain_link_from_mastodon(mastodon_url, domain)
    if not source_link:
        logger.warning(f"No {domain} link found in Mastodon post: {mastodon_url}")
        return False

    data["source"] = source_link

    if not dry_run:
        with Path(filepath).open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    logger.info(f"Updated source to {source_link} in {Path(filepath).name}")
    return True


def correct(config: SyndicationConfig) -> None:
    logger.info("Starting correction operation...")

    syndication_dir = config.paths.syndication_dir
    domain = config.site.domain
    dry_run = config.options.dry_run

    if not Path(syndication_dir).is_dir():
        logger.warning(f"Directory not found: {syndication_dir}")
        return

    corrected = 0
    for filepath in Path(syndication_dir).iterdir():
        if not filepath.name.endswith(".json"):
            continue
        if _correct_json_file(str(filepath), domain, dry_run):
            corrected += 1

    logger.info(f"Corrected {corrected} JSON files")
    logger.info("Correction operation completed")


def correct_from_config(config: SyndicationConfig) -> None:
    correct(config)
