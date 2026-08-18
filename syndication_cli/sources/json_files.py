import json
import logging
from pathlib import Path

from syndication_cli.models import SyndicationConfig
from syndication_cli.utils import find_post_from_source

from .common import add_syndication_to_post

logger = logging.getLogger(__name__)


def process(config: SyndicationConfig) -> list[dict]:
    logger.info(">> Processing JSON files")

    updates = []
    syndication_dir = Path(config.paths.syndication_dir)
    content_dir = config.site.content_dir

    if not syndication_dir.is_dir():
        logger.warning(f"Directory not found: {syndication_dir}")
        return updates

    for filepath in syndication_dir.iterdir():
        if filepath.suffix != ".json":
            continue
        try:
            with Path(filepath).open(encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Error reading {filepath}: {e}")
            continue

        syndication = data.get("syndication", [])
        if isinstance(syndication, str):
            syndication = [syndication]
        elif syndication is None:
            syndication = []

        source = data.get("source")
        if not source or not syndication:
            continue

        post_path = find_post_from_source(source, content_dir)
        if not post_path:
            logger.debug(f"Post not found for source: {source}")
            continue

        added = add_syndication_to_post(post_path, syndication, config.options.dry_run)
        if added:
            logger.info(f"Updated {post_path} from JSON {filepath}")
            updates.append(
                {
                    "file": post_path,
                    "source": source,
                    "syndication": " | ".join(added),
                    "feed": "json",
                }
            )

    return updates
