import hashlib
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


def clean_slug(slug: str) -> str:
    url_without_query = slug.split("?")[0]
    return hashlib.md5(url_without_query.encode("utf-8"), usedforsecurity=False).hexdigest()


def normalize_url(url: str) -> str:
    return url.rstrip("/")


def find_urls(text: str) -> list[str]:
    pattern = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"
    return re.findall(pattern, text)


def parse_fediverse_url(url: str) -> dict | None:
    match1 = re.match(r"https?://([^/]+)/@([^/]+)/(\d+)", url)
    if match1:
        host, username, post_id = match1.groups()
        return {"host": host, "username": username, "id": post_id}

    match2 = re.match(r"https?://([^/]+)/notes/([a-zA-Z0-9]+)", url)
    if match2:
        host, post_id = match2.groups()
        return {"host": host, "username": None, "id": post_id}

    return None


def find_post_from_source(source_url: str, content_dir: str) -> str | None:
    match = re.search(r"https?://[^/]+/(.+?)/?$", source_url)
    if not match:
        return None

    slug_path = match.group(1).rstrip("/")
    folder_path = Path(content_dir) / slug_path

    index_file = folder_path / "index.md"
    if index_file.exists():
        return str(index_file)

    slug_file = Path(content_dir) / (slug_path + ".md")
    if slug_file.exists():
        return str(slug_file)

    return None


def ensure_directory(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)
    logger.debug(f"Directory ensured: {path}")
