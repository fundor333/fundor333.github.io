from taxonomy import collect_values, known_values, set_post_values, update_archetype_values

SERIES_KEY = "series"


def collect_series(content_dir: str = "content/post") -> set[str]:
    """Walk every post's index.md and gather all `series` values used so far."""
    return collect_values(SERIES_KEY, content_dir)


def known_series(archetype_path: str = "archetypes/post.md", content_dir: str = "content/post") -> list[str]:
    """All series known so far: used in a post, or only declared in the archetype.

    Deduplicated and sorted alphabetically (case-insensitive).
    """
    return known_values(SERIES_KEY, archetype_path, content_dir)


def update_archetype_series(
    archetype_path: str = "archetypes/post.md",
    content_dir: str = "content/post",
) -> None:
    """Merge every series found in content/post into the archetype's `series` list,
    deduplicated and sorted alphabetically (case-insensitive)."""
    values = update_archetype_values(SERIES_KEY, archetype_path, content_dir)
    if values is not None:
        print(f"Updated {archetype_path} with {len(values)} series")


def set_post_series(post_path: str, series_list: list[str]) -> None:
    """Overwrite a single post's `series:` list with exactly the given series."""
    set_post_values(post_path, SERIES_KEY, series_list)
