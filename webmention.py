from pathlib import Path
from datetime import datetime, timedelta
import requests
from pprint import pprint
import json
import os

TOKEN = "-g5vlz9y3p5llrdS7TmnCg"
DOMAIN = "fundor333.com"
PER_PAGE = 999
SINCE_DAY = 999

def elaborate_webmention(webmention:list, site:str, remove_paramas: bool):
    for e in webmention["children"]:
        slug = e["wm-target"]

        if remove_paramas is True:
            slug = slug.split('?')[0]

        print(slug)
        
        slug = slug.replace(site, "").replace("\\", "")
        ids= e['wm-id']

        filename = os.path.join(f'data/webmentions/{slug}/{ids}.json')

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(e, f)    


def get_webmention(remove_paramas: bool=True):
    r = requests.get(
        "https://webmention.io/api/mentions.jf2",
        params={'domain': DOMAIN,
        'token':TOKEN,
        'since': datetime.today() - timedelta(days=SINCE_DAY),
        'per-page':PER_PAGE
        }
    )

    elaborate_webmention(webmention=r.json(),site=f"https://{DOMAIN}", remove_paramas=remove_paramas)




get_webmention()
