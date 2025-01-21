import requests
import os
import datetime
import json
from pathlib import Path
import hashlib

http_domain = "https://fundor333.com"
domain = "fundor333.com"
token = os.getenv("WEBMENTIONS_TOKEN")
since_days = 30


now = datetime.datetime.now()
since_data = now - datetime.timedelta(hours=24 * since_days)
url = f"https://webmention.io/api/mentions.jf2?domain={domain}&token={token}&since={since_data.isoformat()}&per-page=999"
all_hash = []


def clean_slug(slug: str):
    return hashlib.md5(
        (slug.split("?")[0]).encode("utf-8"), usedforsecurity=False
    ).hexdigest()


r = requests.get(url)
data = r.json()
output = {}

for webmention in data["children"]:

    with open("temp.json", "w") as fp:

        label = clean_slug(webmention["wm-target"])
        all_hash.append(label)
        label += "/" + str(webmention["wm-id"])

        if output.get(label, False):
            output[label].append(webmention)
        else:
            output[label] = [webmention]

for key in output.keys():
    original_path = key
    path_list = original_path.split("/")

    path_list = [x for x in path_list if x.strip()]
    if path_list != []:
        filename = path_list.pop()

        path_folder = os.path.join("data", "webmentions", *path_list)

        Path(path_folder).mkdir(parents=True, exist_ok=True)
        path_file = os.path.join(path_folder, filename + ".json")

        with open(path_file, "w") as fp:
            json.dump(output[key], fp)


for folder in all_hash:
    path_f = os.path.join("data", "webmentions", folder)

    files = os.listdir(path_f)

    out_dict = []
    for e in files:
        with open(os.path.join(path_f, e)) as file:
            out_dict.append(json.load(file))

    with open(os.path.join("data", "webmentions", folder + ".json"), "w") as fp:
        json.dump(out_dict, fp)
