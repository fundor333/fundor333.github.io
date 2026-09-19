from pathlib import Path

from taxonomy import (
    _extract_values,
    collect_values,
    known_values,
    normalize_spaces_to_dashes,
    set_post_values,
    update_archetype_values,
)

TAGS_KEY = "tags"


def normalize_tag(value: str) -> str:
    """Tags can't contain spaces: collapse them into dashes (e.g. "django rest
    framework" -> "django-rest-framework"). Categories and series keep spaces."""
    return normalize_spaces_to_dashes(value)


def collect_tags(content_dir: str = "content/post") -> set[str]:
    """Walk every post's index.md and gather all `tags` values used so far."""
    return {normalize_tag(v) for v in collect_values(TAGS_KEY, content_dir)}


def known_tags(archetype_path: str = "archetypes/post.md", content_dir: str = "content/post") -> list[str]:
    """All tags known so far: used in a post, or only declared in the archetype.

    Deduplicated case-insensitively and sorted alphabetically.
    """
    return sorted({normalize_tag(v) for v in known_values(TAGS_KEY, archetype_path, content_dir)}, key=str.casefold)


def normalize_existing_post_tags(content_dir: str = "content/post") -> list[str]:
    """Rewrite every post's `tags:` list so spaces become dashes.

    Returns the paths of the posts that were actually changed.
    """
    changed: list[str] = []
    for md_path in Path(content_dir).rglob("index.md"):
        raw = _extract_values(md_path, TAGS_KEY)
        if not raw:
            continue
        normalized = [normalize_tag(v) for v in raw]
        if normalized != raw:
            set_post_values(str(md_path), TAGS_KEY, normalized)
            changed.append(str(md_path))
    return changed


def update_archetype_tags(
    archetype_path: str = "archetypes/post.md",
    content_dir: str = "content/post",
) -> None:
    """Replace spaces with dashes in every post's tags, then merge every tag
    found in content/post into the archetype's `tags` list, deduplicated
    case-insensitively and sorted alphabetically."""
    for path in normalize_existing_post_tags(content_dir):
        print(f"Normalized tags (spaces -> dashes) in {path}")

    values = update_archetype_values(TAGS_KEY, archetype_path, content_dir)
    if values is not None:
        print(f"Updated {archetype_path} with {len(values)} tags")


def set_post_tags(post_path: str, tags_list: list[str]) -> None:
    """Overwrite a single post's `tags:` list with exactly the given tags,
    replacing spaces with dashes."""
    set_post_values(post_path, TAGS_KEY, [normalize_tag(t) for t in tags_list])
