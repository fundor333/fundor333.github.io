import requests
import datetime
import os
import re
import typer
from typing import Annotated


url = "https://api.meetup.com/gql-ext"


query = """query($eventId: ID!) {
    event(id: $eventId) {
      title
      topics {
        edges {
          node {
            id
          }
        }
      }
      description
      dateTime
      endTime
      eventUrl
      eventType
      howToFindUs
      venues {
        name
        address
        city
        country
      }
      group{
        name
      }
    }
  }"""


def fetch_event(event_id):
    variables = {"eventId": event_id}
    r = requests.post(url, json={"query": query, "variables": variables})
    return r.json()


def convert_json_to_post(data):
    # convert the json to a markdown post following the format in content/event

    now = datetime.datetime.now(datetime.UTC)

    event = data["data"]["event"]
    title = event["title"]
    description = event["description"]
    date_time = datetime.datetime.fromisoformat(event["dateTime"].replace("Z", ""))
    end_time = datetime.datetime.fromisoformat(event["endTime"].replace("Z", ""))
    event_url = event["eventUrl"]
    # event_type = event["eventType"]
    how_to_find_us = event["howToFindUs"]
    venues = event["venues"]
    group_name = event["group"]["name"]
    topics = [edge["node"]["id"] for edge in event["topics"]["edges"]]

    tags = [f"meetup-{topic}" for topic in topics]
    tags_str = ", ".join(tags)
    date_str = date_time.strftime("%Y-%m-%d %H:%M:%S")
    end_date_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
    venue_str = ""
    if len(venues) > 1:
        venue = venues[0]
        venue_str = f"{venue['name']}, {venue['city']}, {venue['country']}"
    else:
        venue_str = "Online"

    post = f"""---
title: {title!r}
date: {now.strftime('%Y-%m-%dT%H:%M:%S')}
start: {date_str}
end: {end_date_str}
location: {venue_str}
group:
- {group_name}
tags: [{tags_str}]
event_url: {event_url}
how_to_find_us: {how_to_find_us}
---
    """
    post += f"\n{description}\n"
    # create the content/event directory if it doesn't exist
    os.makedirs("content/event", exist_ok=True)
    # write to a markdown file where is in the format content/event/YYYY-MM-DD-event-title.md

    filename = f"content/event/{date_time.strftime('%Y-%m-%d')}-{re.sub(r'[^a-zA-Z0-9]+', '-', title).strip('-').lower()}.md"
    with open(filename, "w") as f:
        f.write(post)


def add_to_memory(text: str):
    # Save in /data/memory.txt, if not already present, the url pass as argument
    os.makedirs("data", exist_ok=True)
    memory_file = "data/memory.txt"
    if not os.path.exists(memory_file):
        with open(memory_file, "w") as f:
            f.write("")

    with open(memory_file) as f:
        memory = f.read().splitlines()
    if text not in memory:
        with open(memory_file, "a") as f:
            f.write(text + "\n")
        print(f"Added {text} to memory.")
    else:
        print(f"{text} is already in memory.")


def main(
    text: Annotated[str, typer.Argument()] = None,
    memory: Annotated[bool, typer.Option("--memory", "-m")] = False,
):
    if memory:
        if os.path.exists("data/memory.txt"):
            with open("data/memory.txt") as f:
                memory = f.read().splitlines()
            for item in memory:
                print(f"Fetching event {item} from memory...")
                data = fetch_event(item)
                convert_json_to_post(data)
        else:
            print("No memory file found.")
        return
    if text is None:
        text = input("Give me a Meetup event URL or ID: ")
    match = re.search(r"meetup.com/.+?/events/(\d+)", text)
    if match:
        text = match.group(1)
    add_to_memory(text)
    data = fetch_event(text)
    convert_json_to_post(data)


if __name__ == "__main__":
    typer.run(main)
