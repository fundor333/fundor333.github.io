import re
from pathlib import Path

import yaml

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n", re.DOTALL)


def _extract_values(md_path: Path, key: str) -> list[str]:
    """Read a post's front matter and return its `key` entries, if any."""
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

    values = front_matter.get(key)
    if not values:
        return []
    if isinstance(values, str):
        values = [values]
    if not isinstance(values, list):
        return []

    return [v.strip() for v in values if isinstance(v, str) and v.strip()]


def collect_values(key: str, content_dir: str = "content/post") -> set[str]:
    """Walk every post's index.md and gather all `key` values used so far."""
    found: set[str] = set()
    for md_path in Path(content_dir).rglob("index.md"):
        found.update(_extract_values(md_path, key))
    return found


def dedupe_case_insensitive(values) -> set[str]:
    """Collapse values that only differ by case into a single canonical spelling.

    When several casings of the same value exist (e.g. "Ollama" and "ollama"),
    the fully-lowercase spelling wins if present, otherwise the choice is
    deterministic (alphabetical) so repeated runs are stable.
    """
    canonical: dict[str, str] = {}
    for value in sorted(values, key=lambda s: (s.casefold(), s != s.lower(), s)):
        canonical.setdefault(value.casefold(), value)
    return set(canonical.values())


def normalize_spaces_to_dashes(value: str) -> str:
    """Collapse any run of whitespace in `value` into a single dash."""
    return re.sub(r"\s+", "-", value.strip())


def resolve_against_known(raw_value: str, known: list[str]) -> str:
    """Match `raw_value` against `known` case-insensitively.

    Returns the already-known spelling when a case-insensitive match exists,
    so typing "Django" when "django" is already in use reuses "django"
    instead of creating a near-duplicate.
    """
    for candidate in known:
        if candidate.casefold() == raw_value.casefold():
            return candidate
    return raw_value


def _find_block(lines: list[str], key: str) -> tuple[int, list[str], int] | None:
    """Locate the `key:` line in a front-matter-like file and its `- item` lines.

    Returns (index of the `key:` line, existing items, index right after the block).
    """
    target = f"{key}:"
    for i, line in enumerate(lines):
        if line.strip() == target:
            existing = []
            end_idx = i + 1
            while end_idx < len(lines) and lines[end_idx].startswith("- "):
                existing.append(lines[end_idx][2:].strip())
                end_idx += 1
            return i, existing, end_idx
    return None


def _write_block(path: Path, key_idx: int, end_idx: int, lines: list[str], values: list[str]) -> None:
    new_block = [f"- {v}\n" for v in values]
    lines[key_idx + 1 : end_idx] = new_block
    path.write_text("".join(lines), encoding="utf-8")


def known_values(key: str, archetype_path: str = "archetypes/post.md", content_dir: str = "content/post") -> list[str]:
    """All values known so far for `key`: used in a post, or only declared in the archetype.

    Deduplicated case-insensitively and sorted alphabetically (case-insensitive)."""
    archetype = Path(archetype_path)
    lines = archetype.read_text(encoding="utf-8").splitlines(keepends=True)
    block = _find_block(lines, key)
    existing = block[1] if block else []

    all_values = dedupe_case_insensitive(set(existing) | collect_values(key, content_dir))
    return sorted(all_values, key=str.casefold)


def update_archetype_values(
    key: str,
    archetype_path: str = "archetypes/post.md",
    content_dir: str = "content/post",
) -> list[str] | None:
    """Merge every `key` value found in content_dir into the archetype's list,
    deduplicated case-insensitively and sorted alphabetically.

    Returns the resulting sorted list, or None if the archetype has no `key:` block.
    """
    archetype = Path(archetype_path)
    lines = archetype.read_text(encoding="utf-8").splitlines(keepends=True)

    block = _find_block(lines, key)
    if block is None:
        print(f"Could not find a '{key}:' key in {archetype_path}, skipping update")
        return None
    key_idx, existing, end_idx = block

    all_values = dedupe_case_insensitive(set(existing) | collect_values(key, content_dir))
    sorted_values = sorted(all_values, key=str.casefold)

    _write_block(archetype, key_idx, end_idx, lines, sorted_values)
    return sorted_values


def set_post_values(post_path: str, key: str, values: list[str]) -> None:
    """Overwrite a single post's `key:` list with exactly the given values,
    deduplicated case-insensitively and sorted alphabetically."""
    post = Path(post_path)
    lines = post.read_text(encoding="utf-8").splitlines(keepends=True)

    block = _find_block(lines, key)
    if block is None:
        print(f"Could not find a '{key}:' key in {post_path}, skipping")
        return
    key_idx, _existing, end_idx = block

    deduped = sorted(dedupe_case_insensitive(values), key=str.casefold)
    _write_block(post, key_idx, end_idx, lines, deduped)
