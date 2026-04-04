import logging
import sys
from pathlib import Path

import yaml

from .tag_utility import extract_clean_text, genera_tag_seo

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)

DEFAULT_CONTENT_DIR = "content/posts"
DEFAULT_NUM_TAGS = 10


def update_frontmatter_keywords(filepath: str, keywords: list[str], dry_run: bool = False) -> bool:
    with Path(filepath).open("r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return False

    parts = content.split("---", 2)
    if len(parts) < 3:
        return False

    frontmatter_raw = parts[1]
    body = parts[2]

    frontmatter = yaml.safe_load(frontmatter_raw) or {}

    old_keywords = frontmatter.get("keywords", [])
    if isinstance(old_keywords, str):
        old_keywords = [old_keywords]

    frontmatter["keywords"] = keywords

    new_frontmatter = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)

    new_content = f"---\n{new_frontmatter}---{body}"

    if dry_run:
        logger.info(f"[DRY RUN] Would update keywords for {filepath}: {keywords}")
        return True

    with Path(filepath).open("w", encoding="utf-8") as f:
        f.write(new_content)

    logger.info(f"Updated keywords for {filepath}: {keywords}")
    return True


def tagger(config, filepath: str | None = None, dry_run: bool = False, force: bool = False) -> None:
    content_dir = config.site.content_dir

    target_files = [Path(filepath)] if filepath else list(Path(content_dir).rglob("*.md"))

    for file_path in target_files:
        if not file_path.name.startswith("index"):
            continue

        if not force:
            with Path(file_path).open("r", encoding="utf-8") as f:
                content_check = f.read()
            if content_check.startswith("---"):
                parts = content_check.split("---", 2)
                if len(parts) >= 2:
                    frontmatter_check = yaml.safe_load(parts[1]) or {}
                    if frontmatter_check.get("keywords"):
                        logger.info(f"Skipping {file_path}: already has keywords")
                        continue

        logger.info(f"Processing: {file_path}")

        clean_text = extract_clean_text(str(file_path))
        keywords_str = genera_tag_seo(clean_text, DEFAULT_NUM_TAGS)

        if keywords_str.startswith("Errore"):
            logger.error(f"Error generating tags for {file_path}: {keywords_str}")
            continue

        keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]

        update_frontmatter_keywords(str(file_path), keywords, dry_run)
