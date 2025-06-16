---
title: Activitypub vs Webmention Do You Need Them ?
date: 2025-05-16 07:23:27+02:00
feature_link: https://www.midjourney.com/home/
feature_text: by IA Midjourney
description: Some personal thinking about webmention and activitypub and how to use/combine
  them
isStarred: false
tags:
- webmention
- activitypub
- indieweb
categories:
- rant
- dev
images: null
keywords: null
series:
- Tech News
- Indiweb, webmentions and friends
mp-syndicate-to:
- https://brid.gy/publish/twitter
- https://brid.gy/publish/mastodon
- https://news.indieweb.org/en
reply: null
repost: null
like: null
rsvp: null
bookmark: null
comments:
  host: mastodon.social
  username: fundor333
  id: 114516904456408423
syndication:
- https://mastodon.social/@fundor333/114516904456408423
- https://news.indieweb.org/en
---

I have a lot of article about webmention because I implement them on my site/blog. And I use them ad comment, like sistem and more. But more I read about ActivityPub and the Feedverse more I thing it can be a good think to implement it insite your site for your content and for share to the Feedverse.

## Why do it?

One of the best arguments for having a personal ActivityPub site/server is you having a unique identity, don't fragmenting your identity[^1] on multiple Feedverse accounts.

[^1]: Two article about it [Federated/Fragmentated]([Federated/Fragmentated](https://cogdogblog.com/2024/11/federated-fragmentated/?ref=jadin.me)) and [Who is this?](https://jadin.me/who-is-this/)

But I implemented Webmention and stuff like [Brid](https://brid.gy/) for having the likes, comments and all the stuff I have in the ActivityPub about my posts. So why I need to do it?

If I need more reference to your post/article on the Feedverse, Mastodon has a function[^2] for show your account under your link making a link to your profile. It also easy to set up and some platform has a plugin for it (like for Wordpress) or easy articole online for your favorite platfome (for example this is for [Ghost](https://onemanandhisblog.com/2024/10/adding-a-mastodon-author-to-ghost/)).

[^2]: Post about it [Highlighting journalism on Mastodon](https://blog.joinmastodon.org/2024/07/highlighting-journalism-on-mastodon/)

But if you aren't in the FeedVerse you are loosing in a way in to a social media moviment which is groing with major players studing and testing the ground (Meta, Tumblr, with also X/Twitter looking without public testing) and more and more time pass, more and more service integrate the ActivityPub in their social/site/service.

I also have a lot of attention from the tech blogger, where if you don't write about excitement[^3] you are writing about how to implement ActivityPub on your site[^4].

[^3]: Some article about excitement [Why I'm excited about Ghost getting ActivityPub support](https://jadin.me/why-im-excited-about-ghost-getting-activitypub-support/) [The federated One Man & His Blog](https://onemanandhisblog.com/2025/03/the-federated-one-man-his-blog/)
[^4] For example this article [A Guide to Implementing ActivityPub in a Static Site (or Any Website) - Q1 2025 Updates](https://maho.dev/2025/03/a-guide-to-implementing-activitypub-in-a-static-site-or-any-website-q1-2025-updates/)


## And so? I need to integrate this new stuff into my site?

No and yes. If you want a presence in the FeedVerse you need to be active also there but no with a integration with the ActivityPub protocol: you can share it like the "old days".

Also having a ActivityPub implementation somewhere is a resource draining server so you need to think about how much money and time you want to spend on it.

In the end Webmention and ActivityPub are two way to have more interaction with your site but you also need to now which interaction is better for your site.
