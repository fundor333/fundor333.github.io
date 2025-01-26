---
title: "Django List View With Show More"
date: 2022-04-23T11:17:15+02:00
feature_link: "https://unsplash.com/photos/iqLnrFnGjGA"
feature_text: "Photo by Luc Bercoth on Unsplash"
tags:
- django
- coding
- python
- django filter
slug: "django-filter-list-view-with-show-more"
categories:
- dev
- fingerfood
description: "How to have infinite scrolling in Django FilterView"
meta:
series:
- Django tricks
---

Sometime you want to have infinite scrolling in a Django ListView.
And there are good post about this topic on the internet like [this one](https://dev.to/thepylot/infinite-scroll-with-django-d0a) but nothing about infinite scrolling with filters.

## Basic setup

In this tutorial I assume you have a _Product_ django model and a class view like this:

#### model.py

``` python
from django.db import model

class Product(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.title
```

#### views.py

``` python
from django.views.generic.list import ListView

class ProductsView(ListView):
    model = Product
    paginate_by = 2
    context_object_name = 'products'
    template_name = 'product.html'
    ordering = ['title']
```

Following the post by _thepylot_[^2] this is a template for the list view:
[^2]:[Infinite scroll with django](https://dev.to/thepylot/infinite-scroll-with-django-d0a)

#### templates/product_list.html

``` html
        <div class="container">
            <div class="row infinite-container">
                {% for product in products %}
                    <div class="col-md-6 infinite-item">
                        <div class="card mb-4 shadow-sm">
                            <div class="card-body">
                                <h5>{{product.title}}</h5>
                                <p class="card-text">
                                    {{product.description}}
                                </p>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
            {% if page_obj.has_next %}
            <a class="infinite-more-link" href="?page={{ page_obj.next_page_number }}"></a>
            {% endif %}
        </div>


<script src="/static/js/jquery-2.2.4.min.js"></script>
<script src="/static/js/jquery.waypoints.min.js"></script>
<script src="/static/js/infinite.min.js"></script>
<script>
var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    handler: function(direction) {},
    offset: 'bottom-in-view',
    onBeforePageLoad: function () {$('.spinner-border').show();},
    onAfterPageLoad: function () {$('.spinner-border').hide();}
});
</script>
```

The js import here is all from _[Waypoints](http://imakewebthings.com/waypoints/shortcuts/infinite-scroll/)_ and works. But it return the "normal" pagination. If I add a DjangoFilter[^3] this code not work with it. You need to edit the get parameters of the url.

[^3]:[Django Filter Module](https://django-filter.readthedocs.io/en/stable/)

The important parts are:

* _.infinite-more-link_ is matching the "Next Page" url for the pagination
* _.infinite-item_ is a selector string for the singolar item in the list

So for the filter to work we need to change the _infinite-more-link_ link with the parameters of the filter.

## Adding my stuff

We need to create a new tag for add or edit the _get_ parameters of the url.

#### templatetags/app_tags.py

``` python
from django import template

register = template.Library()


@register.simple_tag
def url_replace_diff(request, field, value):
    """
    Give a field and a value and it's update the post parameter for the url accordly
    """
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
```

So you need to change the template like this:

#### templates/product_list.html

``` html
        <div class="container">
            <div class="row infinite-container">
                {% for product in products %}
                    <div class="col-md-6 infinite-item">
                        <div class="card mb-4 shadow-sm">
                            <div class="card-body">
                                <h5>{{product.title}}</h5>
                                <p class="card-text">
                                    {{product.description}}
                                </p>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
            {% if page_obj.has_next %}
              {% load app_tags %}
                <a class="infinite-more-link" href="?{% url_replace_diff request 'page' page_obj.next_page_number %}"></a>
            {% endif %}
        </div>

<script src="/static/js/jquery-2.2.4.min.js"></script>
<script src="/static/js/jquery.waypoints.min.js"></script>
<script src="/static/js/infinite.min.js"></script>
<script>
var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    handler: function(direction) {},
    offset: 'bottom-in-view',
    onBeforePageLoad: function () {$('.spinner-border').show();},
    onAfterPageLoad: function () {$('.spinner-border').hide();}
});
</script>
```

I change the _.infinite-more-link_ url with the new tag for edit the parameters of the filter.
In this way you can have infinite scrolling with Django Filter and Django Pagination.

This is the easy way to do it. Or at least it's the easiest way I can find.

If you can find a better way to do it, please let me know (tweet, email, post with webmention, ...) thanks.
