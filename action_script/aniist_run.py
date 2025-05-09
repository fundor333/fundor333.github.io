import requests
import logging

url = "https://appletune.fundor333.com/weeklynote/anilist/gen"

r = requests.get(url)

logging.info(r.text)
