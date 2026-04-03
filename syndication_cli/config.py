import logging
from pathlib import Path

import yaml

from .models import (
    ExternalConfig,
    FeedConfig,
    HackerNewsConfig,
    OptionsConfig,
    PathsConfig,
    SiteConfig,
    SyndicationConfig,
)


def load_config(config_path: str = "config/syndication.yaml") -> SyndicationConfig:
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with Path(config_file).open(encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    site_data = raw.get("site", {})
    feeds_data = raw.get("feeds", {})
    external_data = raw.get("external", {})
    paths_data = raw.get("paths", {})
    options_data = raw.get("options", {})

    hn_data = external_data.get("hacker_news", {})
    hacker_news = HackerNewsConfig(
        username=hn_data.get("username", ""),
        enabled=hn_data.get("enabled", True),
    )

    indieweb_list = []
    for item in feeds_data.get("indieweb", []):
        indieweb_list.append({"url": item.get("url", ""), "site": item.get("site", "")})

    reddit_username = feeds_data.get("reddit_username") or feeds_data.get("reddit")

    feeds = FeedConfig(
        mastodon=feeds_data.get("mastodon"),
        bluesky=feeds_data.get("bluesky"),
        medium=feeds_data.get("medium"),
        reddit=reddit_username,
        indieweb=indieweb_list,
    )

    return SyndicationConfig(
        site=SiteConfig(
            domain=site_data.get("domain", "https://fundor333.com"),
            content_dir=site_data.get("content_dir", "content"),
        ),
        feeds=feeds,
        external=ExternalConfig(hacker_news=hacker_news),
        paths=PathsConfig(
            syndication_dir=paths_data.get("syndication_dir", "data/syndication"),
            log_file=paths_data.get("log_file", "log_feed.csv"),
        ),
        options=OptionsConfig(
            dry_run=options_data.get("dry_run", False),
            verbose=options_data.get("verbose", False),
        ),
    )


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
