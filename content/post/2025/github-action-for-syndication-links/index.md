---
title: "Github Action for Syndication Links"
date: 2025-01-23T13:22:54+01:00
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
description: "How I have syndications'links fill by the machine"
isStarred: false
tags:
- hugo
- github
- github actiom
categories:
- dev
images:
keywords:
- gohugo
- webmention
- blogging
- hacking
series:
- Hugo tricks
- Indiweb, webmentions and friends
---

A lot of time ago I implement the Webmention in my site following a lot of blogpost.

One of them was a bigger ispiration for my implementation[^indiewebify] and I have some chat with the author of the post over Mastodon for the implementation of the syndications link in a static site[^synd] and how to implement it.

{{< mastodon "https://mastodon.social/@fundor333/108752916197327869">}}

<br><hr>

{{< mastodon "https://fosstodon.org/@chringel/108754642028626230" >}}


After 3 years I find the solution in a post about webmetions!

[^indiewebify]: [Indiewebify me! And don't forget my webmentions!](https://chringel.dev/2022/07/indiewebify-me-and-dont-forget-my-webmentions/)

[^synd]:[dev with the same problem](https://fosstodon.org/@chringel/108754642028626230)

## The input

Paul Kinlan wrote an article in the 2019 which flow under my radar and I didn'read it untile recently[^solution_post].

[^solution_post]: [Using Web Mentions in a static site (Hugo)](https://paul.kinlan.me/using-web-mentions-in-a-static-sitehugo/)

In this post he use a Github action to write the webmention into a data folder for his GoHugo implementation. He has a script which download the data and put into file (the name of the file is the hash of the url of the post) which are use to render the webpage interested by the webmention. And all of this into Github Actions...

So I start thinking about it more and more...
What can I have the syndications links into a file for url? Like the webmention in this post? I need to read the urls form the social media and other stuff.

But now with X/Twitter in bad shape and Facebook/Meta only good for share photos I only use Mastodon so it is easy read them and write a file for url...

A implementation I find is this one by Brandon Rozek[^medium] that I like in a lot of way but I change it because I don't use Medium...

[^medium]: [Syndicating Hugo Posts to Medium](https://brandonrozek.com/blog/syndicating-hugo-to-medium/)

## The implementation

So I start with the development:

1) I need a file type/data structure standard for the Syndication
2) I need a script (or more) that find the syndication's links
3) I need to edit/add to the template some code for the render of it

### Structure data
First are the data structure: json, with the name of the file is an hash of the url

``` json
{
	"syndication": [
		"https://mastodon.social/@fundor333/113809667070052761"
	]
}
```

For example this is my data for [this post](https://fundor333.com/photos/2025/square-square-square-and-square/). I choose Json because I can make check on it and it is a beautiful format for data

### The Scraper script

In this case I find that Mastodon generate a feed for every public profile so I only implementa a reader (class MastodonFinder) which read the feed and save the toots url if find a link to my domain, and a writer class (WriterSyndication) which run all the other class (in this case only the Mastodon one) and write the output as a look-a-like of the json show before.

``` python
import feedparser
from pathlib import Path
import os
import json
import hashlib

domain = "https://fundor333.com"
rss_url_mastodon = "https://mastodon.social/@fundor333.rss"


def clean_slug(slug: str):
    return hashlib.md5(
        (slug.split("?")[0]).encode("utf-8"), usedforsecurity=False
    ).hexdigest()


class MastodonFinder:
    def find_urls(self, string):
        x = string.split('"')
        res = []
        for i in x:
            if i.startswith("https:") or i.startswith("http:"):
                res.append(i)
        return res

    def run(self, rss_url: str, domain: str, output: dict):
        feed = feedparser.parse(rss_url)
        if feed.status == 200:
            for entry in feed.entries:
                link = entry.get("link")
                for e in self.find_urls(entry.get("description")):
                    if domain in e:
                        e = clean_slug(e)
                        if output.get(e, False):
                            output[e].append(link)
                        else:
                            output[e] = [link.strip()]
        else:
            print("Failed to get RSS feed. Status code:", feed.status)


class WriterSyndication:
    def __init__(self, rss_url_mastodon: str, domain: str):
        self.output = {}
        self.rss_url_mastodon = rss_url_mastodon
        self.domain = domain

    def data_gathering(self):
        m = MastodonFinder()
        m.run(self.rss_url_mastodon, self.domain, self.output)

    def write(self):
        for key in self.output.keys():

            path_folder = os.path.join("data", "syndication")

            Path(path_folder).mkdir(parents=True, exist_ok=True)
            path_file = os.path.join(path_folder, key)

            with open(path_file + ".json", "w") as fp:
                json.dump({"syndication": self.output[key]}, fp)

    def run(self):
        self.data_gathering()
        self.write()


w = WriterSyndication(rss_url_mastodon, domain)
w.run()
```

I wrote in this way because I can change the readers or add new one but all the rest of the code remain the same.

#### TODO one bug
Only thing is I need to implement some code for reading all the old file and add to them and not create a new data file if there is an old one.

### The GitHub Action

I run it as a Github Action with this parameters.

``` yaml
name: Syndication Link

on:
  schedule:
    - cron: "0 */2 * * *"
  workflow_dispatch:
jobs:
  webmentions:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@master

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: "pip" # caching pip dependencies

      - name: Install Pip dependencies
        run: pip install -r requirements.txt

      - name: Fetch Syndication
        run: python ./action_script/syndication-collector.py

      - name: Commit to repository
        env:
          GITHUB_TOKEN: ${{ secrets.TOKEN }}
          COMMIT_MSG: |
            👾Fetch webmentions
            skip-checks: true
        run: |
          git config user.email "git@fundor333.com"
          git config user.name "fundor333"
          git remote set-url origin https://x-access-token:${GITHUB_TOKEN}@github.com/fundor333/fundor333.github.io.git
          git checkout main
          git add .
          git diff --quiet && git diff --staged --quiet || (git commit -m "${COMMIT_MSG}"; git push origin main)
```

I always put "workflow_dispatch" as one of the running condiction for having a manual button for running it.

### The template

This is the template fragment I use to show the syndication of one of the post.
It return a single line of text with all the link of the syndication label as the host of the service (as if it is a mastodon.social/xxxx/xxxx link, the label will be mastodon.social).

``` go-html-template
{{ $urlized := .Page.Permalink | md5 }}
{{ if index .Site.Data.syndication $urlized }}

<hr>
<br>
  <div class="syndication">
      <i class="fas fa-link"></i>
      This post was also syndicated to:
      {{ $data:=  index .Site.Data.syndication $urlized  }}

      {{ $data:= $data.syndication }}

      {{ range $index, $url := $data}}
        {{- $parsed_url := urls.Parse $url -}}
        {{- if $index }}, {{- end }}
        <a class="u-syndication" href="{{ $url }}" rel="syndication">{{ $parsed_url.Host }}</a>
      {{ end }}
  </div>
  <br>
{{ end }}
```

I also add the microformat2 tags because all my site has them.

## Conclusion

I love this way and I am happy because I resolve a problem I had with my blog for 3 years
