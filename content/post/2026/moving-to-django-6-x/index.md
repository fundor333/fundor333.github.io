---
title: Moving to Django 6.X
date: 2026-08-24 21:41:59+02:00
feature_link: https://matteoscarpa.it/
feature_text: by Fundor333/Matteo Scarpa/Me
description: Why I upgrade to Django 6.x and why I need it now
isStarred: false
tags:
- django
- python
categories:
- dev
syndication:
- https://mastodon.social/@fundor333/117153152669648998
- https://www.reddit.com/r/django/comments/1vxjtro/why_i_move_to_django_6x_and_why_i_am_more_happy
comments:
  host: mastodon.social
  username: fundor333
  id: '117153152669648998'
keywords:
- Django
- Django tasks
- Django 6.1
- Django 6.0
- async tasks
- task framework
- Redis integration
- model field fetch modes
- template partials
- Htmx
- PostgreSQL 14
- database migration
- dependency updates
- query optimization.
---

A long time ago I start my personal server in Django (a lot of the stuff from [Django tricks](/series/django-tricks/) were coded for my personal Django stuff) and some days ago I decide to upgrade to 6.1 or more. Why?

## New things in 6.0 and 6.1

The main thing in Django 6.0 is the [Django Tasks Frameworks](https://docs.djangoproject.com/en/6.1/topics/tasks/).
Having a unique framework for the async task is a beautifull thing and made me clean a lot of code and make it more pythonic in multiple way.

I update my code for the Task Framework because I need it (I was using a Redis integration) but I want to change the backend without edit all my code so this is the best way to do it because the Django integration for multiple backend are easy to implement and update if needed.

![Modern Time Gif](Charlie_Chaplin_GIF_by_Coolidge_Corner_Theatre.gif)

I also love the new [Model Field Fetch Modes](https://docs.djangoproject.com/en/6.1/releases/6.1/#model-field-fetch-modes). This is cleaner that my abuse of *prefetch_related* and add the FETCH_RAISE which raise error if you fetch data in the wrong section of your code. I don't know if the last one is usefull for me but I do understand the needed for this.

The last thing I was waiting in Django are the [Template Partials](https://docs.djangoproject.com/en/6.1/ref/templates/language/#template-partials). I use something similar a lot on GoHugo for this blog and I understand how a Django module can use it and why I want something so simple but also so usefull for not duplicate code in the frontend.

![CatCoder](CatCodingGIF.gif)

I also know that the template partials are usefull BUT aren't Htmx[^1] so you can mixit with the Template Partials to make easyer manage your frontend and backend.

[^1]: Another blog post about Django and Htmx [Django Table, Filter and Export With Htmx](/post/2026/django-table-filter-export-with-htmx/)


I also thing that the deprecation of PostgreSQL 14 is needed and can fix some vulnerability of my Django project.

## So do I upgrade without problem?

Yes, I haven't got any problem with the upgrade and the migration (PostgreSql14 was my db... Now I upgrade it a lot...) and all my dipendency are updated too...

In the end I am happy of the upgrade. I have less query in the db (I did a lot of not well optimize query) and the cleaner task code is a god sent for update or debugging. Ok I need to debug an async code (same problem of all the async code) but now I have a larger community for answer (yes, I can ask to an AI but I find a lot of the answer inside other blog or StackOverflow so, I can not use an AI, I don't uset it) than than the old module I was using.

Do you upgrade or do you wait more time for the upgrade?
