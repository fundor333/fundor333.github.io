---
title: "Generate Post With Img for Hugo"
date: 2025-07-10T00:36:34+02:00
draft: true
feature_link: "https://www.midjourney.com/home/"
feature_text: ""
description: How I create new post on Hugo and generate an image as cover
isStarred: false
tags:
- image
- hugo
- script
- hacking
categories:
- dev
- fingerfood

images:
keywords:
series:
- Hugo tricks
reply:
repost:
like:
rsvp:
bookmark:
---

Some days ago I find a new post from a blog I follow about "[Open Graph Meta Tags on Hugo and WordPress Blogs](https://www.burgeonlab.com/blog/hugo-and-wordpress-open-graph-meta-tags/)" as a toot

{{< toot instance="fosstodon.org" id="114818281454845557" >}}

and I find I do the same thing and some more. I generate a default cover because I prefer to have a "standard" generated image or a specific image as the feature image. The image set in the settings is a default, a  "if all other image fall use this" kind of stuff.

## How I generate the post?

When I write a post I launch a [makefile command](/post/2021/the-team-makefile/)
