from dataclasses import dataclass, field


@dataclass
class SiteConfig:
    domain: str
    content_dir: str


@dataclass
class FeedConfig:
    mastodon: str | None
    bluesky: str | None
    medium: str | None
    reddit: str | None
    indieweb: list = field(default_factory=list)


@dataclass
class HackerNewsConfig:
    username: str
    enabled: bool


@dataclass
class ExternalConfig:
    hacker_news: HackerNewsConfig


@dataclass
class PathsConfig:
    syndication_dir: str
    log_file: str


@dataclass
class OptionsConfig:
    dry_run: bool = False
    verbose: bool = False


@dataclass
class SyndicationConfig:
    site: SiteConfig
    feeds: FeedConfig
    external: ExternalConfig
    paths: PathsConfig
    options: OptionsConfig


@dataclass
class SyndicationEntry:
    source: str | None = None
    syndication: list[str] = field(default_factory=list)


@dataclass
class PostInfo:
    file_path: str
    source_url: str
    syndication_links: list[str]
    feed_source: str


@dataclass
class FediversePost:
    host: str
    username: str | None
    post_id: str
