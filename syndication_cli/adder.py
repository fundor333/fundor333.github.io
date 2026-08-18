import csv
import logging
from pathlib import Path

from .models import SyndicationConfig
from .sources import add_syndication_to_post, bluesky, json_files, mastodon, medium, reddit
from .utils import find_post_from_source

logger = logging.getLogger(__name__)


def add_mention(source_url: str, destination_url: str, config: SyndicationConfig) -> dict | None:
    content_dir = config.site.content_dir

    post_path = find_post_from_source(source_url, content_dir)
    if not post_path:
        logger.error(f"Post not found for source: {source_url}")
        return None

    added = add_syndication_to_post(post_path, [destination_url], config.options.dry_run)
    if not added:
        logger.info(f"No new mention added to {post_path} (already present?)")
        return None

    logger.info(f"Added mention {destination_url} to {post_path}")
    return {
        "file": post_path,
        "source": source_url,
        "syndication": " | ".join(added),
        "feed": "manual",
    }


def add(config: SyndicationConfig) -> None:
    logger.info("Starting add operation...")
    log = []

    log += json_files.process(config)
    log += mastodon.process(config)
    log += bluesky.process(config)
    log += medium.process(config)
    log += reddit.process(config)

    if log:
        log_file = config.paths.log_file
        with Path(log_file).open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["file", "source", "syndication", "feed"])
            writer.writeheader()
            writer.writerows(log)
        logger.info(f"Log saved to {log_file}")
    else:
        logger.info("No updates made")

    logger.info("Add operation completed")


def add_from_config(config: SyndicationConfig) -> None:
    add(config)
