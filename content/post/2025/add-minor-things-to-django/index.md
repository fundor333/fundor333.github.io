---
title: "Add Minor Things to Django for templating"
date: 2025-06-15T21:36:00+02:00
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
description: Some code I use in my django project for having some utility
isStarred: false
tags:
- django
- coding
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

comments:
  host: mastodon.social
  username: fundor333
  id: 114689582471095983
---

More and more time I need some little thing for templating:

- The date fild of a form with the right input type for the page
- A link with all the get parameters of the current page (form, paginator, etc...) and one added


## The Code

This little code is mine but you can use it on all your project without thinking. If you find an error comment or webmention or replay with activity pub to my toot

### Date Field for Django Form

This is the widget I add to the django form for adding the right input type.

``` python
from django.forms import TextInput

class DateInput(TextInput):
    input_type = "date"
```

I need this because the css/js framework I use add a data picker if you fill the input_type

### Tag for change/keep a field

Sometime I need to edit or add a get parameter in a link, like when you change the view from list to grid (for example).
So I coded this simple tag.

``` python
from django import template
register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
```

the only thing it does is change or add a value into the list of existing value.

For example

``` jinja
<a href:"https://fundor333.com?{% url_replace_diff request 'page' page_obj.page_number %}">Link</a>
```

In this one I pass the pagination number to the new page. Why? Because I need to have the current page and all the serch filter also in the new page and this is the cleaner way WITHOUT using Js (I need control and Js is not controll)
