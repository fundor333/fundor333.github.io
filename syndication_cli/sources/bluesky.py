import logging

from syndication_cli.models import SyndicationConfig

from .common import process_rss_feed

logger = logging.getLogger(__name__)


def process(config: SyndicationConfig) -> list[dict]:
    feed_url = config.feeds.bluesky
    if not feed_url:
        return []

    logger.info(">> Processing Bluesky")
    return process_rss_feed(feed_url, "bluesky", config)
