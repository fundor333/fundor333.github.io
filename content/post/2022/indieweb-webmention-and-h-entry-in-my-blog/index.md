---
title: "How I implement Indieweb, Webmention and H Entry in My Blog"
date: 2022-06-16T13:02:46+02:00
feature_link: "https://unsplash.com/photos/en4qp-aK1h4"
feature_text: "Photo by Mae Mu on Unsplash"
tags:
- indiweb
- webmention
- h-entry
- hugo
- twtxt
slug: "indieweb-webmention-and-h-entry-in-my-blog"
categories:
- dev
- coding
description: "Adding Indieweb and Webmention in my blog"
type: "post"
---

## Some history of this blog

When I start blogging, I was using a blog engine called [WordPress](https://wordpress.org/) but I wasn't ok with the way it was designed. I wanted to be able to write my posts in a way that was easy to read and edit. I want to have a lightweight blog engine so I change to [Pelican](https://blog.getpelican.com/) and I use for sometime. Sometime later, not happy with the tags and categories, I decided to switch to [Hugo](https://gohugo.io/) and I'm happier with it.

But I feet some time I wasn't happy with Hugo so I search something else.
After some time I find an article about [Independent website](https://victoria.dev/blog/make-your-own-independent-website/) and the tecnology for make a independent website.

In this article I discover:

* [*Twtxt*](https://github.com/buckket/twtxt) a protocol for instances for a decentralized timeline experience
* [*Webmention*](Webmention) and an [easy implementation](https://github.com/aaronpk/webmention.io) for it
* [*IndieWeb*](https://indieweb.org/POSSE) for POSSE, an abbreviation for Publish (on your) Own Site, Syndicate Elsewhere

So I decided to study them for adding in my blog.

## Twtxt

First tecnology I read about and I found it strange.

It call himself *decentralises, minimalist microblogging service for hackers* but it is only a txt file in your domain. Something like this:

``` txt
2016-02-04T13:30:00+01:00   You can really go crazy here! ┐(ﾟ∀ﾟ)┌
2016-02-03T23:05:00+01:00   @<example <http://example.org/twtxt.txt>> welcome to twtxt!
2016-02-01T11:00:00+01:00   This is just another example.
2015-12-12T12:00:00+01:00   Fiat lux!
```

You can "tweet" from your domain to the world... It is a good idea but I don't like it.

I was using it for a time but I prefer to use [mastodon](https://mastodon.social/@fundor333) or webmention.

Also it isn't compatible with my stack for the blog (my github pages builder aren't compatible with twtxt without rewrite all my stack) and I don't like the way it is implemented: it is a good idea to have a decentralized timeline but I prefere something easy to use anda update with a mobile phone or a tablet unlike twtxt.

So I decided to study the others tecnologies.

## Webmention

My favorite tecnology of the article.

> Webmention is a simple way to notify any URL when you mention it on your site. From the receiver's perspective, it's a way to request notifications when other sites mention it.
>
> [Webmention w3c specification](https://www.w3.org/TR/webmention/)

This is a wonderfull way to interact between two websites. You can use it to send a notification to a third party when you mention it on your site or to send a notification to your site when you mention it on a third party site.

You can use to check also interaction with your twitter, mastodon, reddit and github with some tools like [Bridgy](https://brid.gy/).

### Implementation

Thanks to [Jamie's post](https://www.jayeless.net/2021/02/integrating-webmentions-into-hugo.html),[Jamie's post](https://www.jvt.me/posts/2019/03/18/displaying-webmentions/) and [Paul's post](https://paul.kinlan.me/using-web-mentions-in-a-static-sitehugo/) I implemented my own display section for the webmentions.

I wrote and rewrote the code for the display section but now it's something simple:

for getting the webmentions from [Webmention.io](https://webmention.io/) I use the js package [PlaidWeb/webmention.js](https://github.com/PlaidWeb/webmention.js/) with some changes for the rendering.

#### theme/layouts/partials/webmentions.html

``` html
<script src="/webmention.min.js" data-wordcount="100" async="" data-add-urls="https://fundor333.com{{ .RelPermalink}}">
</script>

<div id="webmentions" class="row">
</div>
```

I suggest to download and edit the [*webmention.min.js*](https://github.com/PlaidWeb/webmention.js/) file for adding some customizations for the rendering and add some CSS because the basic theme is minimal.

With this code imported, you can show the webmention feed on your site in real time.

## Indiweb

Realy the big thing and the last thing I studied and implement.
It is "*a people-focused alternative to the corporate web*" and it has three core concepts:

* Your content is yours
* You are better connected
* You are in control

I {{< heart >}} it.

So I rewrote all my templates to implement the Indiweb concept:

0. Find a domain for my space
1. Adding an [h-card/microformat](https://indieweb.org/h-card) to my homepage
2. Adding an [h-card/microformat](https://indieweb.org/h-card) to my posts' articles
3. Adding the social media profiles for implementing the [IndieAuth identity](https://indieweb.org/How_to_set_up_web_sign-in_on_your_own_domain)
4. Adding RSS feeds and/or other type of feeds

After one or two month of work on my template the work was done and I was happy.
And I search for more posts about indiweb and webmentions because I WANT MORE, so I find a lot of articles, posts and tweet about this stack of tecnologies.

One of my favorite posts about indiweb is [AM I ON THE INDIEWEB YET? by Miriam Suzanne](https://www.miriamsuzanne.com/2022/06/04/indiweb/).

Here are some more articles I find about webmentions:

* [Adding Webmention Support to a Static Site](https://keithjgrant.com/posts/2019/02/adding-webmention-support-to-a-static-site/)
* [Adding Webmentions to My Static Hugo Site](https://anaulin.org/blog/adding-webmentions/)
* [Adding Webmentions to my blog](https://hugo.md/post/add-webmentions-to-hugo-from-micro-blog/)
* [Adding Webmentions to My Static Hugo Site](https://anaulin.org/blog/adding-webmentions/)
* [Microblogging](https://paulrobertlloyd.com/articles/2018/01/microblogging/)
