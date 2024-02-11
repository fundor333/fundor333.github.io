---
title: "Django Return Pdf With Reportlab"
date: 2022-02-28T11:13:30+01:00
feature_link: "https://unsplash.com/photos/n2ILm0aTCYo"
feature_text: "Photo by Hannes Wolf on Unsplash"
tags:
- coding
- django
- reportlab
slug: "django-return-pdf-with-reportlab"
categories:
- dev
- fingerfood
description: "How to print a pdf with Django and return it from url"
type: "post"
meta:
- pdf
- python
Focus_Keyword: "django pdf reportlab"
---

Sometime you need to print a pdf from your site or your web app with some custom data.
In Python you can make pdf with ReportLab[^1][^2] and some other module but I _LOVE_ ReportLab[^3].

## What do I need?

You only need _Django and ReportLab_

``` bash
pip install django
pip install reportlab
```

## Write the pdf

When you have the requirements you can write the code for the pdf.
For example this is a example of a class for printing A6 pdf

``` python3
from reportlab.lib.pagesizes import A6, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate

class CustomDocTemplate(SimpleDocTemplate):
    def __init__(
        self,
        filename,
        right_margin=7,
        left_margin=7,
        top_margin=7,
        bottom_margin=7,
        pagesize=landscape(A6),
        **kw,
    ):
        super().__init__(filename, **kw)
        self.rightMargin = right_margin
        self.leftMargin = left_margin
        self.topMargin = top_margin
        self.bottomMargin = bottom_margin
        self.pagesize = pagesize


class A6Printer:
    def get_pdf(self, buffer):
        self.buffer = buffer
        styles = getSampleStyleSheet()
        doc = CustomDocTemplate(buffer)
        elements = []
        elements.append(Paragraph("Title of the PDF", style=styles["Heading2"]))
        elements.append(Paragraph("Heading", style=styles["Heading4"]))
        elements.append(Paragraph("Text inside the pdf", style=styles["BodyText"]))
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
```

## Make the view

Now we need a view for Django. Usualy I write ClassView so this is an example for the printer define in the last example.

``` python3
from django.views import View


class A6View(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="Example.pdf"'
        a6p = A6Printer()
        pdf = a6p.get_pdf(BytesIO())
        response.write(pdf)
        return response
```

With this ClassView you can download a generated pdf with static data, dinamic data or some static and some dynamic data. I am working on more post about Reportlab so if you have some suggestion or question Tweet me.
Thanks

[^1]: [Official site of ReportLab](https://www.reportlab.com/)
[^2]: Famous library for python. I wrote an article about it some time ago [Letterhead With ReportLab]({{< relref "/post/2021/letterhead-with-reportlab.md" >}})
[^3]: You can read more [ReportLab: PDF Processing with Python](https://www.blog.pythonlibrary.org/books/reportlab-pdf-processing-with-python/)
