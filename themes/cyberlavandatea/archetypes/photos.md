+++
title = "{{ replace .File.ContentBaseName `-` ` ` | title }}"
date = {{ .Date }}
draft = true
description = ""
tags = ["photos"]
# Add the images as a page bundle. An optional exif.json can sit next to them:
#   { "IMG_0001.jpg": { "model": "…", "lensmodel": "…", "aperture": "f/2.8", … } }
+++
