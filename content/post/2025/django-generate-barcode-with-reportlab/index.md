---
title: "Django Generate Barcode With Reportlab"
date: 2025-05-21T08:59:51+02:00
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
description: Tutorial to build pages and pages of barcode for labeling stuffs
tags:
- reportlab
- django
- barcode
- qrcode
categories:
- dev

images:
keywords:
series:
- Printing With ReportLab
- Django tricks

draft: true
reply:
repost:
like:
rsvp:
bookmark:
---

After [Django With Barcode and Qrcode]({{% ref "/post/2022/django-with-barcode-and-qrcode" %}}) and [Django Return Pdf With Reportlab]({{% ref "http://localhost:1313/post/2022/django-return-pdf-with-reportlab" %}}) I need something new in my Django server. I need a barcode generator for labeling stuffs.

## The problem

Every code is a solution to a pratical problem. In this case I need to make the barcode labels with text for keep an inventory.
The basic solution is generate a pdf/img file to print into sticker's paper and cut it after.

![Barcode Example](barcode.png)

So, I need the data to convert into lable (the string on top to the barcode) and the barcode (or the qrcode) as in the screenshot, so I wrote this code for do it for pages and ready to print and stick it all around the world!

## Code

