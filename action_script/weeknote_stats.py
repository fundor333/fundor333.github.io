import datetime
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

import frontmatter

weeknotes_dir = Path("content/weeknotes")
stats_file = Path("data/weeknote_stats.json")

# My own blogs: they are in every weeknote, so they are not counted.
own_domains = {"fundor333.com", "digitaltearoom.com", "matteoscarpa.it", "matteoscarpa.com"}

# Fixed sections repeated in every weeknote (not suggestions).
skipped_sections = {"My Links", "Currently Reading"}

link_re = re.compile(r"(?<!!)\[[^\]]*\]\((https?://[^)\s]+)\)")
heading_re = re.compile(r"^##\s+(.*)$")


def normalize_domain(url: str) -> str:
    domain = urlparse(url).netloc.lower()
    return domain.removeprefix("www.")


def extract_domains(body: str) -> list[str]:
    domains = []
    section = None
    for line in body.splitlines():
        heading = heading_re.match(line)
        if heading:
            section = heading.group(1).strip()
            continue
        if section in skipped_sections:
            continue
        for url in link_re.findall(line):
            domain = normalize_domain(url)
            if domain and domain not in own_domains:
                domains.append(domain)
    return domains


def weeknote_id(path: Path) -> str:
    # content/weeknotes/2026/40/index.md -> 2026/40
    return f"{path.parent.parent.name}/{path.parent.name}"


def compute_stats() -> dict:
    links = defaultdict(int)
    weeks = defaultdict(set)
    first_seen = {}
    last_seen = {}
    total_weeknotes = 0
    total_links = 0

    for path in sorted(weeknotes_dir.glob("*/*/index.md")):
        post = frontmatter.load(path)
        if post.get("draft"):
            continue
        total_weeknotes += 1
        date = str(post.get("date", ""))[:10]
        week = weeknote_id(path)
        for domain in extract_domains(post.content):
            total_links += 1
            links[domain] += 1
            weeks[domain].add(week)
            if domain not in first_seen or date < first_seen[domain]:
                first_seen[domain] = date
            if domain not in last_seen or date > last_seen[domain]:
                last_seen[domain] = date

    blogs = [
        {
            "domain": domain,
            "links": links[domain],
            "weeknotes": len(weeks[domain]),
            "weeknotes_share": round(len(weeks[domain]) / total_weeknotes, 4) if total_weeknotes else 0,
            "first_seen": first_seen[domain],
            "last_seen": last_seen[domain],
        }
        for domain in links
    ]
    blogs.sort(key=lambda b: (-b["links"], -b["weeknotes"], b["domain"]))
    for rank, blog in enumerate(blogs, start=1):
        blog["rank"] = rank

    return {
        "updated": datetime.date.today().isoformat(),
        "excluded_domains": sorted(own_domains),
        "total_weeknotes": total_weeknotes,
        "total_links": total_links,
        "unique_blogs": len(blogs),
        "blogs": blogs,
    }


def update_stats() -> dict:
    stats = compute_stats()
    stats_file.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n")
    print(
        f"Updated {stats_file}: {stats['unique_blogs']} blogs, "
        f"{stats['total_links']} links in {stats['total_weeknotes']} weeknotes"
    )
    return stats


if __name__ == "__main__":
    update_stats()
