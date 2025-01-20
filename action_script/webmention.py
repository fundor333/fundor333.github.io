import requests
import os
import datetime
import json
from pathlib import Path


http_domain = "https://fundor333.com"
domain = "fundor333.com"
token = os.getenv('WEBMENTIONS_TOKEN')
since_days = 30


now = datetime.datetime.now()
since_data = now - datetime.timedelta(hours=24 * since_days)
url = f"https://webmention.io/api/mentions.jf2?domain={domain}&token={token}&since={since_data.isoformat()}&per-page=999"

print(url)


def clean_slug(slug: str):
    return slug.replace(http_domain, "").split("?")[0]


r = requests.get(url)

data = r.json()

output = {}

for webmention in data["children"]:

    with open('temp.json', 'w') as fp:

        label = clean_slug(webmention['wm-target'])

        if output.get(label, False):
            output[label].append(webmention)
        else:
            output[label] = [webmention]

for key in output.keys():
    original_path = key
    path_list = original_path.split('/')

    path_list = [x for x in path_list if x.strip()]
    if path_list != []:
        filename = path_list.pop()

        path_folder = os.path.join('data', "webmentions", *path_list)

        Path(path_folder).mkdir(parents=True, exist_ok=True)
        path_file = os.path.join(path_folder, filename + ".json")

        with open(path_file, 'w') as fp:
            json.dump(output[key], fp)
