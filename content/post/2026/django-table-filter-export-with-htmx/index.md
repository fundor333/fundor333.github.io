---
title: "Django Table Filter Export With Htmx"
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

```django
import logging
from django.db.models import Sum
from django.http import Http404
from django.utils.timezone import now
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    MonthArchiveView,
    TemplateView,
    UpdateView,
)
from django_tables2 import SingleTableMixin
from django_tables2.export import ExportMixin, TableExport



class DataHtmx(ExportMixin, SingleTableMixin, FilterView):
    table_class = DataTable
    model = DataModel

    template_name = "generic/table2.html"

    filterset_fields = ["info","created_at", "updated_at"]

    export_formats = (
        TableExport.CSV,
        TableExport.XLS,
        TableExport.XLSX,
        TableExport.ODS,
    )


    def get_export_filename(self, export_format):
        return f"Export Data.{export_format}"
```


```jinja
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
