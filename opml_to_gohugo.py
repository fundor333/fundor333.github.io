from bs4 import BeautifulSoup
import json

# Reading the data inside the xml
# file to a variable under the name
# data
with open('my-feeds.opml', 'r') as f:
    data = f.read()

# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object
Bs_data = BeautifulSoup(data, "xml")

# Finding all instances of tag
# `unique`
b_unique = Bs_data.find_all('outline')

out = {}
title = ""
for item in b_unique:
    if item.attrs.get("xmlUrl", False) is False:
        title = item.attrs.get("title")
        out[title] = []
    else:
        out[title].append({"title": item.attrs.get("title"), "url": item.attrs.get("xmlUrl")})

data = []
for key in out.keys():
    if len(out[key]) > 0:
        data.append({"elements": out[key], "type": key})


with open("data/raw_hoarding.json", "r") as outfile:
    data_other = json.load(outfile)
    print(len(data_other))

data += data_other
print(len(data))

json_object = json.dumps(data, indent=4)

# Writing to sample.json
with open("data/feed.json", "w") as outfile:
    outfile.write(json_object)
