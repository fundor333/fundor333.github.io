+++
title = "{{ replace .File.ContentBaseName `-` ` ` | title }}"
date = {{ .Date }}
draft = true
description = ""
tags = ["photos"]
# Metti le immagini come page bundle. exif.json opzionale accanto ad esse:
#   { "IMG_0001.jpg": { "model": "…", "lensmodel": "…", "aperture": "f/2.8", … } }
+++
