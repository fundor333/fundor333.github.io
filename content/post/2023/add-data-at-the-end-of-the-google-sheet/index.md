---
title: "Add Data at the End of the Google Sheet"
date: 2023-07-25T12:35:10+02:00
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
tags:
- script
- google drive
- google api
slug: "add-data-at-the-end-of-the-google-sheet"
categories:
- dev
description: "How I write a row of data at the end of a Google Sheet with Python Api"
type: "post"
mp-syndicate-to:
- https://brid.gy/publish/twitter
- https://brid.gy/publish/mastodon
images:
keywords:
---

Some time ago, for work, I need to add a row (or more) at the END of a google sheet in an automatic way.

Searching on-line I did't find any post or StackOverflow about adding row at the end of the sheet so here we are.

## Before you start

This tutorial expect you to have follow the [Google prerequisit's post](https://developers.google.com/workspace/guides/create-credentials) so please follow it.

In our case we need:

* a API Key with writing power 
* the email for the project (create with the app)
* a gsheet with data

You need to add the email of the project as editor for the gsheet

## The code

Fist we need to import all the library and have a setup of the constant of the script.
In this case

```python
import datetime
import logging
from typing import List
import pygsheets

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]
SERVICE_ACCOUNT_FILE = "account.json"
```

So we need a function insert my data in the gsheet so I declered a function and define the gsheet as sheet

```python
def add_to_sheet(spreadsheet_id: int, worksheet_title:str, data=list[dict]):

    client = pygsheets.authorize(service_file=SERVICE_ACCOUNT_FILE)
    sheet = client.open_by_key(spreadsheet_id)
```

Now I need to set a *pointer* (in this case *i*) at the first row empty (k.a.k. the one after the last wrote row)

``` python

    wks = sheet.worksheet_by_title(worksheet_title)
    all_values = wks.get_all_values()

    i = 0
    for e in all_values:
        if "".join(e) != "":
            i += 1
```

After all this preparation you can cycle through your data for the writing phase and we have

``` python
    for element in data:
        wks.insert_rows(
            i,
            values=[
                element['col1'],
                element['col2'],
                element['col3'],
                element['col4'],
            ],
            inherit=True,
        )
        done.append(element.id)
        i += 1
```

If you did all right now you have a function for write at the end of your gsheet data.You can use as is or you can combine it with other in to bigger project.

## Conclusions

For easy access this is the full code, write me if you have problems

```python
import datetime
import logging
from typing import List
import pygsheets

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]
SERVICE_ACCOUNT_FILE = "account.json"


def add_to_sheet(spreadsheet_id: int, worksheet_title:str, data=list[dict]):

    client = pygsheets.authorize(service_file=SERVICE_ACCOUNT_FILE)
    sheet = client.open_by_key(spreadsheet_id)

    wks = sheet.worksheet_by_title(worksheet_title)
    all_values = wks.get_all_values()

    i = 0
    for e in all_values:
        if "".join(e) != "":
            i += 1

    for element in data:
        wks.insert_rows(
            i,
            values=[
                element['col1'],
                element['col2'],
                element['col3'],
                element['col4'],
            ],
            inherit=True,
        )
        done.append(element.id)
        i += 1
```
