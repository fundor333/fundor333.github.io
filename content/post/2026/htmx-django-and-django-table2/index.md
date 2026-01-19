---
title: Htmx Django and Django Table2
date: 2026-01-19 12:33:09+01:00
feature_link: https://www.midjourney.com/home/
feature_text: by IA Midjourney
description: How I use Htmx for showing in a Django project a django-table2 filled
  with data from a MonthArchiveView
isStarred: false
tags:
- django
- htmx
- django-table2
- montharchiveview
categories:
- rant
- dev
images: null
keywords: null
series:
- Django tricks
syndication:
- https://mastodon.social/@fundor333/115921577107907407
comments:
  host: mastodon.social
  username: fundor333
  id: '115921577107907407'
---

For some time I am developing my personal Django server. It keeps some data for me and it is my automation server. And I want to test a Htmx code on Django so I make a little thing in my personal django project.

## What I have

I have a MonthArchiveView with render a table list with a lot of function I need: add element, change month show, exports query as files, etc...

I also don't like to reload all the page for change the month I am seeing on the page.
So I start to implement what I need.

And, from some comment from the web and some friends, I want less code and more clean one.

## What I used

For this project I used:

- **Django** the framework used[^1]
- **Django Table2** a module for easy creation of table for Django[^2]
- **Django Htmx** a module for easy support of Htmx[^3]
- **Tablib** a module for exporting the table as multiple file type[^4]

[^1]: [Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source](https://www.djangoproject.com/)
[^2]: [django-tables2 - An app for creating HTML tables](https://github.com/jieter/django-tables2)
[^3]: [django-htmx Extensions for using Django with htmx](https://pypi.org/project/django-htmx/)
[^4]: [Tablib: format-agnostic tabular dataset library](https://pypi.org/project/tablib/)


### The Py code

So I start with the code for the model. It need to have a DateTimeField or a DateField (this becose I want to have an MonthArchiveView view).


~~~ python >
# blog/model.py

class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    content = models.TextAreaField()
    date = models.DateTimeField(auto_now_add=True)
~~~

and after I add the code for the table with the ordering of the data

~~~ python
# blog/tables.py

import django_tables2 as tables
from blog.models import Post

class PostTable(tables.Table):
    class Meta:
        model = Post
        order_by = ("-date", "title")
        fields = ["date", "title", "slug"]

~~~

After the model and the table we need the view called by the HTMX code.

I set all the config for choose the right data field and which is the format for month and year, followed for the export types' settings.


~~~ python
# blog/views.py

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableView, tables
from blog.models import Post
from blog.tables import PostTable

class PostMonthArchiveHtmx(LoginRequiredMixin, ExportMixin, SingleTableMixin, MonthArchiveView):
    model = Post
    template_name = "generic/table2_with_export.html"
    table_class = PostTable


    date_field = "date"
    allow_future = True
    month_format = "%m"
    year_format = "%Y"
    allow_empty = True

    export_formats = (
    TableExport.CSV,
    TableExport.XLS,
    TableExport.XLSX,
    TableExport.ODS,)

    def get_month(self):
        try:
            month = super().get_month()
        except Http404:
            month = now().strftime(self.get_month_format())

        return month

    def get_year(self):
        try:
            year = super().get_year()
        except Http404:
            year = now().strftime(self.get_year_format())

        return year

    def get_export_filename(self, export_format):
        return f"Export Post {self.get_year()}-{self.get_month()}.{export_format}"

~~~

I added a function for changing the name of the output file (because I like filename with date reference) and two functions for setting month and year if not given (we need them later for the Htmx part).

### The Jinja part

After the python code I wrote this generic template for all my django-table2 table (in this case with the export code)

~~~ django
# templates/generic/table2_with_export.html

{% load render_table from django_tables2 %}
{% load export_url from django_tables2 %}

<div>
    {% for format in view.export_formats %}
    <a href="{{ request.path }}{% export_url format %}" target="_blank">
      <code>{{ format }}</code>
    </a>
    {% endfor %}
    <hr>
    {% render_table table %}
</div>
~~~

I take out all the css stuff so you can add your style and/or css classes.

At this point we have all we need to have a html page with the table and the exports we need. We only need to add this view into the urls...

For example this is a generic example for a urls file for this project

~~~ python
# blog/urls.py

from django.urls import path

from blog.views import (
    PostMonthArchiveHtmx,
)

app_name = "blog"

urlpatterns = [

    path("htmx/post", PostMonthArchiveHtmx.as_view(month_format="%m",name="htmx-post")),
]

~~~

You can see that I didn't add the code for having the month and the year in the url. This is because I had a lot of problems with the next part and this is the cleanest way I found to code this.

### The Htmx fragment

I will assume that you have done the quickstart form Htmx's site[^5] because I don't want to write about Htmx...

[^5]: [htmx in a Nutshell](https://htmx.org/docs/#introduction)


So for using inside a Django project for calling the page with Htmx we need to add the csrf token inside the header of the request so I added inside the main tag for my project.

It resembles this fragment.

~~~ html
<!-- template/base.html -->

<!-- Other part of the template-->

<div hx-headers='{"x-csrftoken": "{{ csrf_token }}"}'>
  {% block content %}
    (no content)
  {% endblock %}
</div>

<!-- Other part of the template-->

~~~

So now I need to write the div for the Htmx. And this is what I wrote:

~~~ html

<div hx-get="{% url 'blog:htmx-post' %}?year={{ month|date:"Y" }}&month={{ month|date:"m" }}&{{ request.GET.urlencode }}"
     hx-trigger="load">This will be replaced.</div>
~~~

I build the url in the hx-get in a strange way because I need to add the query input for the MonthArchiveView (the &month and &year field in the url) and add all the other field. In this way I also have the sorting links in the header of the table working.


## Conclusion

This is how I have combine this 3 libs for my personal project and if you find it useful share it. Thanks!
