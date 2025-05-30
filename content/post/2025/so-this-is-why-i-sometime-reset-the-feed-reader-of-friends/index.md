---
title: "So This Is Why I Sometime Reset the Feed Reader of Friends"
date: 2025-05-31T12:32:59+02:00
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
description: I find something I didn't know abouts feed rss and atom
isStarred: false
tags:
- feed
- atom
- rss
- coding
categories:
- rant
images:
keywords:
series:

reply:
repost:
like:
rsvp:
bookmark:

comments:
  host: mastodon.social
  username: fundor333
  id:
---

I have a friend who read my blog using my feed. And sometime he pings me for some problem with the feed, like a drop of all the article as new

{{<mastodon "https://social.lol/@robb/113854214799861227">}}

{{<mastodon "https://mastodon.social/@andreagrandi/113854638640440084" >}}

And after read some other post with the same problem ( [Robb Knight problem with feed reader](https://rknight.me/notes/202501190902/) [Kev other problem with feed reader](https://kevquirk.com/notes/20250528-1702?utm_source=fundor333.com&utm_medium=link&utm_campaign=blogging&ref=fundor333.com) ) I understand a little this: Atom is newer and superior than Rss.

## Atom vs Rss

Atom is the newer one, born after the RSS and after fix a lot of the RSS bugs like:

- You have a strict format for checking and validation in Atom
- RSS is simpler but less strict and it is riddled with ambiguities which lead to inconsistency of interpretation
- You have a unique id for the feed in Atom

The last one is the one I was searching...

## The Answer

The feed reader find the new feed (new because you change the url or you change the serverside code) and check:

- Atom Feed: the reader find the same ID so is the same feed
- RSS Feed: the reader don't find the ID and find something different not in the items part so it is a new one

So I add the JsonFeed and AtomFeed to the blog for give the reader multiple option for the feed!

You can find all at [this link]({{< ref "feeds">}})
