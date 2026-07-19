import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import frontmatter
import requests
import typer
from bs4 import BeautifulSoup

http_domain = "https://fundor333.com"
weeknotes_dir = Path("content/weeknotes")

# Own domains: never send a webmention to ourselves (e.g. the "My Links"
# section or the "New post from my blog" self-link).
own_domains = {
    "fundor333.com",
    "www.fundor333.com",
    "digitaltearoom.com",
    "matteoscarpa.it",
    "ko-fi.com",
}

link_re = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)\)")


def is_own_domain(url: str) -> bool:
    return urlparse(url).netloc.lower() in own_domains


def extract_links(body: str) -> list[str]:
    links = []
    for url in link_re.findall(body):
        if not is_own_domain(url) and url not in links:
            links.append(url)
    return links


def discover_webmention_endpoint(target: str) -> str | None:
    try:
        r = requests.get(target, timeout=10, allow_redirects=True)
    except requests.exceptions.RequestException as e:
        print(f"    ! could not fetch target {target}: {e}")
        return None

    link_header = r.links.get("webmention")
    if link_header:
        return urljoin(r.url, link_header["url"])

    soup = BeautifulSoup(r.content, "html.parser")
    tag = soup.find(["link", "a"], rel="webmention", href=True)
    if tag:
        return urljoin(r.url, tag["href"])

    return None


def send_webmention(source: str, target: str, dry_run: bool) -> None:
    endpoint = discover_webmention_endpoint(target)
    if not endpoint:
        print(f"    - no webmention endpoint for {target}")
        return

    if dry_run:
        print(f"    (dry-run) would POST to {endpoint} source={source} target={target}")
        return

    try:
        r = requests.post(endpoint, data={"source": source, "target": target}, timeout=10)
        if r.ok:
            print(f"    + sent webmention to {endpoint} (target={target}, status={r.status_code})")
        else:
            print(f"    ! webmention rejected by {endpoint} (target={target}, status={r.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"    ! failed to send webmention to {endpoint} for {target}: {e}")


def process_weeknote(year: int, week: int, dry_run: bool) -> None:
    post_path = weeknotes_dir / str(year) / str(week) / "index.md"
    if not post_path.exists():
        print(f"! weeknote {year}/{week} not found, skipping")
        return

    post = frontmatter.load(post_path)
    links = extract_links(post.content)
    source = f"{http_domain}/weeknotes/{year}/{week}/"

    print(f"Weeknote {year}/{week}: {len(links)} link(s) to mention (source={source})")
    for target in links:
        print(f"  -> {target}")
        send_webmention(source, target, dry_run)


def latest_weeknote() -> tuple[int, int]:
    years = sorted(
        (int(p.name) for p in weeknotes_dir.iterdir() if p.is_dir() and p.name.isdigit()),
        reverse=True,
    )
    for year in years:
        weeks = sorted(
            (int(p.name) for p in (weeknotes_dir / str(year)).iterdir() if p.is_dir() and p.name.isdigit()),
            reverse=True,
        )
        if weeks:
            return year, weeks[0]
    raise FileNotFoundError("No weeknote posts found")


def weeks_in_year(year: int) -> list[int]:
    year_dir = weeknotes_dir / str(year)
    if not year_dir.is_dir():
        raise FileNotFoundError(f"No weeknote posts found for year {year}")
    return sorted(int(p.name) for p in year_dir.iterdir() if p.is_dir() and p.name.isdigit())


def main(
    year: int = typer.Argument(None, help="Year of the weeknote(s). Omit to use the latest post."),
    week: int = typer.Argument(None, help="Week number. Requires year. Omit to process the whole year."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Discover endpoints but don't send anything."),
) -> None:
    if year is None:
        year, week = latest_weeknote()
        process_weeknote(year, week, dry_run)
    elif week is None:
        for w in weeks_in_year(year):
            process_weeknote(year, w, dry_run)
    else:
        process_weeknote(year, week, dry_run)


if __name__ == "__main__":
    typer.run(main)
