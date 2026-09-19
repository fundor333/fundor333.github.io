from taxonomy import collect_values, known_values, set_post_values, update_archetype_values

TAGS_KEY = "tags"


def collect_tags(content_dir: str = "content/post") -> set[str]:
    """Walk every post's index.md and gather all `tags` values used so far."""
    return collect_values(TAGS_KEY, content_dir)


def known_tags(archetype_path: str = "archetypes/post.md", content_dir: str = "content/post") -> list[str]:
    """All tags known so far: used in a post, or only declared in the archetype.

    Deduplicated case-insensitively and sorted alphabetically.
    """
    return known_values(TAGS_KEY, archetype_path, content_dir)


def update_archetype_tags(
    archetype_path: str = "archetypes/post.md",
    content_dir: str = "content/post",
) -> None:
    """Merge every tag found in content/post into the archetype's `tags` list,
    deduplicated case-insensitively and sorted alphabetically."""
    values = update_archetype_values(TAGS_KEY, archetype_path, content_dir)
    if values is not None:
        print(f"Updated {archetype_path} with {len(values)} tags")


def set_post_tags(post_path: str, tags_list: list[str]) -> None:
    """Overwrite a single post's `tags:` list with exactly the given tags."""
    set_post_values(post_path, TAGS_KEY, tags_list)
