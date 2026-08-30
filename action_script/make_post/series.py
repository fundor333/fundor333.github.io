import re
from pathlib import Path

import yaml

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n", re.DOTALL)


def _extract_series(md_path: Path) -> list[str]:
    """Read a post's front matter and return its `series` entries, if any."""
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError:
        return []

    match = FRONT_MATTER_RE.match(text)
    if not match:
        return []

    try:
        front_matter = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return []

    series = front_matter.get("series")
    if not series:
        return []
    if isinstance(series, str):
        series = [series]
    if not isinstance(series, list):
        return []

    return [s.strip() for s in series if isinstance(s, str) and s.strip()]


def collect_series(content_dir: str = "content/post") -> set[str]:
    """Walk every post's index.md and gather all `series` values used so far."""
    found: set[str] = set()
    for md_path in Path(content_dir).rglob("index.md"):
        found.update(_extract_series(md_path))
    return found


def _find_series_block(lines: list[str]) -> tuple[int, list[str], int] | None:
    """Locate the `series:` key in a front-matter-like file and its `- item` lines.

    Returns (index of the `series:` line, existing items, index right after the block).
    """
    for i, line in enumerate(lines):
        if line.strip() == "series:":
            existing = []
            end_idx = i + 1
            while end_idx < len(lines) and lines[end_idx].startswith("- "):
                existing.append(lines[end_idx][2:].strip())
                end_idx += 1
            return i, existing, end_idx
    return None


def _write_series_block(path: Path, series_idx: int, end_idx: int, lines: list[str], series_list: list[str]) -> None:
    new_block = [f"- {s}\n" for s in series_list]
    lines[series_idx + 1 : end_idx] = new_block
    path.write_text("".join(lines), encoding="utf-8")


def known_series(archetype_path: str = "archetypes/post.md", content_dir: str = "content/post") -> list[str]:
    """All series known so far: used in a post, or only declared in the archetype.

    Deduplicated and sorted alphabetically (case-insensitive).
    """
    archetype = Path(archetype_path)
    lines = archetype.read_text(encoding="utf-8").splitlines(keepends=True)
    block = _find_series_block(lines)
    existing = block[1] if block else []

    all_series = set(existing) | collect_series(content_dir)
    return sorted(all_series, key=str.casefold)


def update_archetype_series(
    archetype_path: str = "archetypes/post.md",
    content_dir: str = "content/post",
) -> None:
    """Merge every series found in content/post into the archetype's `series` list,
    deduplicated and sorted alphabetically (case-insensitive)."""
    archetype = Path(archetype_path)
    lines = archetype.read_text(encoding="utf-8").splitlines(keepends=True)

    block = _find_series_block(lines)
    if block is None:
        print(f"Could not find a 'series:' key in {archetype_path}, skipping update")
        return
    series_idx, existing, end_idx = block

    all_series = set(existing) | collect_series(content_dir)
    sorted_series = sorted(all_series, key=str.casefold)

    _write_series_block(archetype, series_idx, end_idx, lines, sorted_series)
    print(f"Updated {archetype_path} with {len(sorted_series)} series")


def set_post_series(post_path: str, series_list: list[str]) -> None:
    """Overwrite a single post's `series:` list with exactly the given series."""
    post = Path(post_path)
    lines = post.read_text(encoding="utf-8").splitlines(keepends=True)

    block = _find_series_block(lines)
    if block is None:
        print(f"Could not find a 'series:' key in {post_path}, skipping")
        return
    series_idx, _existing, end_idx = block

    _write_series_block(post, series_idx, end_idx, lines, sorted(series_list, key=str.casefold))
