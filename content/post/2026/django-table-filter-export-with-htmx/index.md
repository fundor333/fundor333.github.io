---
title: "Django Table, Filter and Export With Htmx"
date: 2026-04-02T16:21:34+02:00
draft: true
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
description:
isStarred: false
tags:
- django
- export
- htmx
- django-table2
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

Some time ago I wrote a [blog post](<{{< relref "post/2026/htmx-django-and-django-table2.md" >}}>) about Htmx and Django-table2

``` python
# blog/model.py

class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    content = models.TextAreaField()
    date = models.DateTimeField(auto_now_add=True)
```

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

``` python
# blog/views.py

from django_tables2 import SingleTableMixin
from django_tables2.export import ExportMixin, TableExport
from django_filters.views import FilterView
from blog.model import Post

class DataHtmx(ExportMixin, SingleTableMixin, FilterView):
    table_class = PostTable
    model = Post

    template_name = "generic/table2.html"

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


``` django
<div hx-get="{% url 'example:home' %}?date_at={{ query_ddate | date:"Y-m-d"  }}&hide_filter" hx-trigger="load">
```

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
