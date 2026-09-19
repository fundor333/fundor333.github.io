from taxonomy import collect_values, known_values, set_post_values, update_archetype_values

CATEGORIES_KEY = "categories"


def collect_categories(content_dir: str = "content/post") -> set[str]:
    """Walk every post's index.md and gather all `categories` values used so far."""
    return collect_values(CATEGORIES_KEY, content_dir)


def known_categories(archetype_path: str = "archetypes/post.md", content_dir: str = "content/post") -> list[str]:
    """All categories known so far: used in a post, or only declared in the archetype.

    Deduplicated case-insensitively and sorted alphabetically.
    """
    return known_values(CATEGORIES_KEY, archetype_path, content_dir)


def update_archetype_categories(
    archetype_path: str = "archetypes/post.md",
    content_dir: str = "content/post",
) -> None:
    """Merge every category found in content/post into the archetype's `categories` list,
    deduplicated case-insensitively and sorted alphabetically."""
    values = update_archetype_values(CATEGORIES_KEY, archetype_path, content_dir)
    if values is not None:
        print(f"Updated {archetype_path} with {len(values)} categories")


def set_post_categories(post_path: str, categories_list: list[str]) -> None:
    """Overwrite a single post's `categories:` list with exactly the given categories."""
    set_post_values(post_path, CATEGORIES_KEY, categories_list)
