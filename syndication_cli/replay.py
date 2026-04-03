import logging
import os
import re
from pathlib import Path
from urllib.parse import urlparse

import frontmatter
import requests
from bs4 import BeautifulSoup

from .models import SyndicationConfig

logger = logging.getLogger(__name__)

MAX_LENGTH = 800


def get_instance_and_id(url: str) -> tuple[str | None, str | None]:
    parsed_url = urlparse(url)
    instance = parsed_url.netloc if parsed_url.netloc else None

    if not instance:
        return None, None

    path_segments = parsed_url.path.strip("/").split("/")

    if len(path_segments) >= 2 and path_segments[0].startswith("@"):
        if len(path_segments) == 2:
            if path_segments[1].isdigit():
                return instance, path_segments[1]
            return instance, path_segments[0]
        if (
            (len(path_segments) > 2 and path_segments[1] == "statuses" and path_segments[2].isdigit())
            or len(path_segments) > 2
            and path_segments[2].isdigit()
        ):
            return instance, path_segments[2]

    elif (
        len(path_segments) >= 3
        and path_segments[0] == "web"
        and path_segments[1] == "statuses"
        and path_segments[2].isdigit()
    ):
        return instance, path_segments[2]

    elif (
        len(path_segments) >= 4
        and path_segments[0] == "users"
        and path_segments[2] == "statuses"
        and path_segments[3].isdigit()
    ):
        return instance, path_segments[3]

    if path_segments:
        if path_segments[-1].isdigit():
            return instance, path_segments[-1]
        if path_segments[0].startswith("@") and len(path_segments) == 1:
            return instance, path_segments[0]

    return instance, None


def get_page_content(url: str) -> str | None:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None


def extract_preview_from_html(html_content: str, max_length: int = MAX_LENGTH) -> str:
    if not html_content:
        return ""

    soup = BeautifulSoup(html_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    text = ""

    e_content_element = soup.find(class_="e-content")
    if e_content_element:
        text = e_content_element.get_text()
    else:
        p_summary_element = soup.find(class_="p-summary")
        if p_summary_element:
            text = p_summary_element.get_text()

    text = re.sub(r"\s+", " ", text).strip()

    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def is_mastodon_link(url: str) -> bool:
    if "@" in url:
        return True

    mastodon_keywords = [
        "mastodon",
        "masto",
        "social",
        "toot",
        "floss.social",
        "fosstodon",
        "pleroma.social",
    ]

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname.lower() if parsed_url.hostname else ""

    return any(keyword in hostname for keyword in mastodon_keywords)


def process_hugo_markdown_files(root_dir: str, dry_run: bool = False) -> None:
    modified_count = 0

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith((".md", ".markdown")):
                continue

            filepath = Path(dirpath) / filename
            logger.debug(f"Processing: {filepath}")

            modified = False

            try:
                with Path(filepath).open(encoding="utf-8") as f:
                    post = frontmatter.load(f)

                if "reply" in post.metadata and post.metadata["reply"]:
                    reply_url = post.metadata["reply"]
                    logger.debug(f"Found reply URL: {reply_url}")

                    if is_mastodon_link(reply_url):
                        if post.metadata.get("mastodon_reply") is not True:
                            post.metadata["mastodon_reply"] = True
                            instance, post_id = get_instance_and_id(reply_url)
                            post.metadata["mastodon_instance"] = instance
                            post.metadata["mastodon_id"] = post_id
                            modified = True
                            logger.info(f"Added mastodon_reply flag for {reply_url}")
                    elif post.metadata.get("mastodon_reply") is True:
                        del post.metadata["mastodon_reply"]
                        del post.metadata["mastodon_instance"]
                        del post.metadata["mastodon_id"]
                        modified = True
                        logger.info("Removed mastodon_reply flag (no longer Mastodon)")

                    html_content = get_page_content(reply_url)
                    if html_content:
                        preview_text = extract_preview_from_html(html_content)
                        if preview_text:
                            if post.metadata.get("preview_text_from_reply") != preview_text:
                                post.metadata["preview_text_from_reply"] = preview_text
                                modified = True
                                logger.debug("Updated preview text")
                        else:
                            if "preview_text_from_reply" in post.metadata:
                                del post.metadata["preview_text_from_reply"]
                                modified = True
                    else:
                        if "preview_text_from_reply" in post.metadata:
                            del post.metadata["preview_text_from_reply"]
                            modified = True

                else:
                    if "preview_text_from_reply" in post.metadata:
                        del post.metadata["preview_text_from_reply"]
                        modified = True
                    if "mastodon_reply" in post.metadata:
                        del post.metadata["mastodon_reply"]
                        modified = True

                if modified:
                    if not dry_run:
                        with Path(filepath).open("wb") as f_write:
                            frontmatter.dump(post, f_write)
                    modified_count += 1
                    logger.info(f"Saved changes to {filename}")

            except Exception as e:
                logger.error(f"Error processing {filepath}: {e}")

    logger.info(f"Processed {modified_count} files")


def replay(config: SyndicationConfig) -> None:
    logger.info("Starting replay processing...")
    content_dir = config.site.content_dir

    if not Path(content_dir).is_dir():
        logger.warning(f"Content directory not found: {content_dir}")
        return

    process_hugo_markdown_files(content_dir, config.options.dry_run)
    logger.info("Replay processing completed")


def replay_from_config(config: SyndicationConfig) -> None:
    replay(config)
