---
title: Generate Post With Img for Hugo
date: 2025-07-12 08:36:34+02:00
feature_link: https://www.midjourney.com/home/
feature_text: ''
description: How I create new post on Hugo and generate an image as cover
tags:
- image
- hugo
- script
- hacking
categories:
- dev
- fingerfood
images: null
keywords: null
series:
- Hugo tricks
reply: null
repost: null
like: null
rsvp: null
bookmark: null
syndication:
- https://mastodon.social/@fundor333/114838916912095814
comments:
  host: mastodon.social
  username: fundor333
  id: '114838916912095814'
---

Some days ago I find a new post from a blog I follow about "[Open Graph Meta Tags on Hugo and WordPress Blogs](https://www.burgeonlab.com/blog/hugo-and-wordpress-open-graph-meta-tags/)" as a toot

{{< toot instance="fosstodon.org" id="114818281454845557" >}}

and I find I do the same thing and some more. I generate a default cover because I prefer to have a "standard" generated image or a specific image as the feature image. The image set in the settings is a default, a  "if all other image fall use this" kind of stuff.

## How I generate the post?

When I write a post I launch a [makefile command]({{< ref "post/2021/the-team-makefile" >}}) and it launch two command for me:

1. Generate a new post with hugo new
2. Generate a cover with my python script

## Some code

For this project I use a font ([Futura Book font](https://font.download/font/futura-book)) and a image where put the title and other thing of the post (for now only the title).
This is the image "clean", without the text.

![cover-blank.jpg](cover-blank.jpg)

``` python
from PIL import Image, ImageDraw, ImageFont  # 👉️ Import modules from PIL


def generate_img(message: str, path: str):
    font_path = "Futura Book font.ttf"  # 👉️ Font .ttf Path
    font_size = 100  # 👉️ Font Size
    img = Image.open("cover-blank.jpg")  # 👉️ Open Image
    dr = ImageDraw.Draw(img)  # 👉️ Create New Image
    my_font = ImageFont.truetype(font_path, font_size)  # 👉️ Initialize Font
    text_x = (img.width) // 2
    text_y = (img.height) // 2
    dr.text((text_x, text_y), message, font=my_font, fill=(255, 255, 255), anchor="mm")
    print("Generated content/" + path + "/cover.png")
    img.save("content/" + path + "/cover.png")
```

This script use Python (the library is PIL) and I set the fill parameters for a standard size OpenGraph image.

If you use a python script for generate new post you can implement this code inside of the script or you can add some code to make a command line to launch after your "new post" command.
