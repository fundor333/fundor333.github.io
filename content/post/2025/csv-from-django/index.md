---
title: "Csv From Django"
date: 2025-04-19T12:23:09+02:00
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
description: A little class view for return CSV
isStarred: false
tags:
- csv
- django
categories:
- dev
- fingerfood
images:
keywords:
series:
- Django tricks

reply:
repost:
like:
rsvp:
bookmark:
---

Some time you need to export a file into a specific format for some use like upload to the old system.
In this case I need to have a CSV file which another software fill.

## The code

I wrote a ClassView for this case, this class. [^1]

[^1]: I don't like coding functional view so I only code ClassViews

``` python
class CsvCarsDownload(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="cars.csv"'
        my_dict = [{
          "brand": "Ford",
          "model": "Mustang",
          "year": 1964
        }]
        writer = csv.DictWriter(
            response, dialect="excel", fieldnames=my_dict[0].keys()
        )
        writer.writeheader()
        for element in my_dict:
          writer.writerow(element)
        return response
```

You can change the type of the the CSV changing the __dialect__ with one of the type of the CSV dialect (excel, excel_tab, unix_dialect) and changing the __my_dict__ with any type of list of dict.

With this code you can use any Class Mixin from others module for add other functions like permission supports or loggeer configurations.
