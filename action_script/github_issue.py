import requests
import json
import os
import logging
from typing import Any


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def search_issues_github(website: str) -> dict[str, Any]:
    query = '"' + website + '" in:body,title type:issue, -author:fundor333 '
    logger.info(f"Query: {query}")
    api_url = "https://api.github.com/search/issues"

    params: dict = {
        "q": query,
        "s": "created",
        "order": "desc",
    }

    found_issues = []
    page = 1
    max_pages = 10

    os.makedirs(os.path.join("data", "github"), exist_ok=True)

    while page <= max_pages:
        params["page"] = page
        logger.debug(f"Fetching page {page}...")
        try:
            response = requests.get(api_url, params=params, timeout=15)
            # Raises an exception for HTTP errors (4xx or 5xx)
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])
            logger.debug(f"Page {page} returned {len(items)} items.")

            if not items:
                logger.info(
                    f"No more results found after page {page - 1}. Stopping search."
                )
                break

            for issue in items:
                reduced_issue = {
                    "id": issue.get("id"),
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "url": issue.get("html_url"),
                    "repository": issue.get("repository_url", "").replace(
                        "https://api.github.com/repos/", ""
                    ),
                    "created_at": issue.get("created_at"),
                    "state": issue.get("state"),
                    "author": issue.get("user", {}).get("login"),
                    "body": issue.get("body"),
                }
                found_issues.append(reduced_issue)

                file_path = os.path.join(
                    "data", "github", str(issue.get("id")) + ".json"
                )
                try:
                    with open(file_path, "w", encoding="utf-8") as fp:
                        json.dump(reduced_issue, fp, ensure_ascii=False, indent=4)
                    logger.debug(f"Saved issue {issue.get('id')} to {file_path}")
                except OSError as file_err:
                    logger.error(
                        f"❌ Error writing file for issue {issue.get('id')}: {file_err}"
                    )

            page += 1

        except requests.exceptions.RequestException as e:
            error_message = f"🛑 API Request Error: {e}"
            logger.error(error_message)
            return {
                "status": "error",
                "details": error_message,
                "issues_found": len(found_issues),
            }

    result_summary = f"✅ Found {len(found_issues)} GitHub issues."
    logger.info(result_summary)
    return {
        "status": "success",
        "result_summary": result_summary,
        "issues_found": len(found_issues),
        "website": website,
    }


WEBSITE_TO_SEARCH = "fundor333.com"
search_result = search_issues_github(website=WEBSITE_TO_SEARCH)
logger.info(search_result)
