---
title: "Message and Allert With Django and Boostrap"
date: 2022-05-02T12:21:50+02:00
feature_link: "https://unsplash.com/photos/M7NajHCqZDM?utm_source=unsplash&utm_medium=referral&utm_content=creditShareLink"
feature_text: "Photo by Anita Jankovic on Unsplash"
tags:
- django
- coding
- boostrap
slug: "message-and-allert-with-django-and-boostrap"
categories:
- dev
- fingerfood
description: "How to use Django messages with Boostrap5"

meta:
- message
- allert
---

Sometime you need to send an allert/message from your Django project to the user, like a popup or a gui message for an user interaction ("Sent the mail", "Done the task", ...) and you want to make it with style (Boostrap in this case).

So this is my code.

## Basic setup settings.py

Check if in the settings you have:

* _django.contrib.messages_ is in _INSTALLED_APPS_
* _django.contrib.sessions.middleware.SessionMiddleware_ and _django.contrib.messages.middleware.MessageMiddleware_ are in _MIDDLEWARE_
* The _context_processors_ option of the DjangoTemplates backend defined in your _TEMPLATES_ setting contains _django.contrib.messages.context_processors.messages_

This is the standard configuration for _django messages_ [^1] and we need to add some config for Boostrap.

[^1]: [Official Django messages documentation](https://docs.djangoproject.com/en/4.0/ref/contrib/messages/)

We need to add the config for the class css for mapping the _Boostrap allert_ with the _Django messages_. You can also add more messages level if you need.

``` python
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }
```

## Adding a Template

We need some html for the templates. I wrote this code and add in the top part of all my pages so I can show messages everywhere in my project

``` python
{% for message in messages %}
  <div class="container-fluid p-0">
    <div class="alert {{ message.tags }} alert-dismissible fade show" role="alert">
      {{ message }}
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
  </div>
{% endfor %}
```

This fragment use Boostrap5 allerts[^2] but you can use your favorite CSS framework for your code
[^2]: [Boostrap5 Allerts](https://getbootstrap.com/docs/5.0/components/alerts/)
