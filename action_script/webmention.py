import requests
import os
import datetime
import json
from pathlib import Path
import hashlib


http_domain = "https://fundor333.com"
domain = "fundor333.com"
token = os.getenv("WEBMENTIONS_TOKEN")
since_days = 360 * 20  # 31


class WebmentionFinder:
    def __init__(self, http_domain: str, token: str, domain: str, since_days: int):
        self.now = datetime.datetime.now()
        self.since_data = self.now - datetime.timedelta(hours=24 * since_days)
        self.all_hash = []
        self.http_domain = http_domain
        self.domain = domain
        self.token = token
        self.url = (
            f"https://webmention.io/api/mentions.jf2?domain={self.domain}"
            + f"&token={self.token}&since={self.since_data.isoformat()}&per-page=999"
        )

    def __clean_slug(self, slug: str):
        return hashlib.md5(
            (slug.split("?")[0]).encode("utf-8"), usedforsecurity=False
        ).hexdigest()

    def __get_data(self):
        r = requests.get(self.url)
        data = r.json()
        self.output = {}

        for webmention in data.get("children", []):

            label = self.__clean_slug(webmention["wm-target"])
            self.all_hash.append(label)
            label += "/" + str(webmention["wm-id"])

            if self.output.get(label, False):
                self.output[label].append(webmention)
            else:
                self.output[label] = [webmention]

    def __generate_files(self):

        for key in self.output.keys():
            original_path = key
            path_list = original_path.split("/")

            path_list = [x for x in path_list if x.strip()]
            if path_list != []:
                filename = path_list.pop()

                path_folder = os.path.join("data", "webmentions", *path_list)

                Path(path_folder).mkdir(parents=True, exist_ok=True)
                path_file = os.path.join(path_folder, filename + ".json")

                with open(path_file, "w") as fp:
                    json.dump(self.output[key], fp)

    def __clean_files(self):

        for folder in self.all_hash:
            path_f = os.path.join("data", "webmentions", folder)

            files = os.listdir(path_f)

            out_dict = {
                "source": [],
                "stats": {
                    "like-of": 0,
                    "bookmark-of": 0,
                    "mention-of": 0,
                    "repost-of": 0,
                    "in-reply-to": 0,
                    "comments": [],
                },
            }
            source = []
            for e in files:
                with open(os.path.join(path_f, e)) as file:
                    for element in json.load(file):
                        source.append(element)

            out_dict["source"] += source
            comments = []
            links = []

            for e in source:
                wm_property = e["wm-property"]
                out_dict["stats"][wm_property] += 1
                link = e["wm-source"]
                if e.get("content", False):
                    if not (link in links):
                        single_data = {
                            "content": e["content"]["text"],
                            "link": e["wm-source"],
                            "author_name": e["author"]["name"],
                            "author_photo": e["author"]["photo"],
                            "author_url": e["author"]["url"],
                        }
                        comments.append(single_data)
                        links.append(link)
            out_dict["stats"]["comments"] = comments

            with open(os.path.join("data", "webmentions", folder + ".json"), "w") as fp:
                json.dump(out_dict, fp)

    def run(self):
        self.__get_data()
        self.__generate_files()
        self.__clean_files()


wb = WebmentionFinder(
    http_domain=http_domain, token=token, since_days=since_days, domain=domain
)
wb.run()
