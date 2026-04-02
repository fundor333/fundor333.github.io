---
title: "Django Table, Filter and Export With Htmx"
date: 2026-04-03T8:21:34+02:00
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
description: A little code fragment for show how to use in the same project Htmx, Django-table2 e Django-filters
tags:
- django
- export
- htmx
- django-table2
- django-filters
- django-filters
categories:
- dev
- fingerfood
series:
- Django tricks
---

Some time ago I wrote a [blog post](<{{< relref "post/2026/htmx-django-and-django-table2.md" >}}>) about Htmx and Django-table2 and all went well...

![So So](soso.gif)

No he didn't work as I wanted so I did some editing of the code here and there.

## The old one

We start with the code I didn't change:

First the model

``` python
# blog/model.py

class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    content = models.TextAreaField()
    date = models.DateTimeField(auto_now_add=True)
```

The table

``` python
# blog/tables.py

import django_tables2 as tables
from blog.models import Post

class PostTable(tables.Table):
    class Meta:
        model = Post
        order_by = ("-date", "title")
        fields = ["date", "title", "slug"]

```

This two fragment are perfect as is so I didn't touch them. But all the other part I reworked as I needed.

## The new parts

I need to have a "universal table" for show data, with filter and export the data.
And I need to have an "universal template" for all the combination Table-Export-Filter...

So I wrote one

![Typing](typing.gif)

First thing (after the model and the table) I need view with filter and exporter support. And using _django-table2_[^1] all was easy.[^2]

[^1]: [Django-table2](https://django-tables2.readthedocs.io/en/latest/)
[^2]: I also use [tablib](https://tablib.readthedocs.io/en/stable/) for the export and [django-filter](https://django-filter.readthedocs.io/en/stable/) for the filtering.

So I wrote this class which support all I need for using it as Htmx endpoint.

``` python
# blog/views.py

from django_tables2 import SingleTableMixin
from django_tables2.export import ExportMixin, TableExport
from django_filters.views import FilterView
from blog.model import Post

class DataHtmx(ExportMixin, SingleTableMixin, FilterView):
    model = Post
    template_name = "generic/table2.html"

    table_class = PostTable

    filterset_fields = ["title","slug", "date"]

    export_formats = (
        TableExport.CSV,
        TableExport.XLS,
        TableExport.XLSX,
        TableExport.ODS,
    )

    def get_export_filename(self, export_format):
        return f"Export Data.{export_format}"
```

- _ExportMixin_, with the _export_formats_ are the the export part of the view
- _SingleTableMixin_ is the table part of the view
- _FilterView_ is the filter part of the view, with _filterset_fields_ as the field you can filter. You can also haave a filterset_class if you need

Done this I need a template. More generic template because I don't want to rewrite the same code every time...

So here is it!

``` django
# templates/generic/table.html

{% load render_table from django_tables2 %}
{% load export_url from django_tables2 %}
{% load django_bootstrap5 %}

{% if filter  %}
  {% if 'hide_filter' not in request.GET %}
      <div class="col-12 col-md-9">
        <div class="card mb-4">
          <div class="card-header">
            <button class="btn btn-section" type="button" data-bs-toggle="collapse" data-bs-target="#filterCollapse">
              <i class="fa-solid fa-filter"></i> Filtri <i class="fa-solid fa-chevron-down"></i>
            </button>
          </div>
          <div id="filterCollapse" class="collapse">
            <div class="card-body">
              <form method="get" class="row">
                {% load django_bootstrap5 %}
                {% bootstrap_form filter.form layout='floating' %}
                  {% include 'generic/_btn_search.html' %}
              </form>
            </div>
          </div>
        </div>
      </div>
{% endif %}
{% endif %}

<div class="row">
    {% if 'hide_export' not in request.GET %}
      {% for format in view.export_formats %}
      <a  class="btn col col-sm" href="{{ request.path }}{% export_url format %}" target="_blank">
        <i class="fa-duotone fa-regular fa-download"></i> <code>{{ format }}</code>
      </a>
      {% endfor %}
    {% endif %}
    <hr>
    {% render_table table %}
</div>
```

This template work if you have filters, export or not.

- the load are for django-table2 and boostrap (the last is for me, is not needed for the code)
- _'hide_filter' not in request.GET_ check if the url has the params for _hide_filter_. If it is present, the template hides the filters
- _'hide_export' not in request.GET_ check if the url has the params for _hide_export_. If it is present, the template hides the exports

One example for the Htmx code is the following.

``` django
<div hx-get="{% url 'blog:post_htmx' %}?date_at={{ query_date | date:"Y-m-d"  }}&hide_filter" hx-trigger="load">
```

In this example I had the filter set (with data form the template) and with _hide_filter_ which hide the filters but not the exports button.


I thing this will be a stable of my django code and it can be move in a custom module for share and easy import.
