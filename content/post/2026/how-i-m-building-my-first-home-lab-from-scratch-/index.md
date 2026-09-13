---
title: "How I Am Building My First Home Lab From Scratch"
date: 2026-09-15T10:32:09+02:00
feature_link: https://matteoscarpa.it/
feature_text: by Fundor333/Matteo Scarpa/Me
description: "Follow my journey as I build my first home lab from scratch. Discover the hardware I chose, the software I'm running, and why every developer needs one."
isStarred: false
tags:
- homelab
- selfhosting
- hacking
categories:
- rant
- dev
- tinkering
series:
- My Home Automation Lab
---

It is some time I am tinking of selfhosting some stuff and more and more time I read post/see video about HomeLabs. So I start thinking about making one.

So what is a HomeLab?

> A homelab is a self-contained IT environment that you design and control. It usually includes basic infrastructure like compute, storage, and networking, along with a hypervisor or virtualization layer (container). Some setups are modest and run on a single machine, while others resemble mini datacenters with multiple nodes and a shared storage such as SAN or NAS.
>
> [StorMagic - What Is a Homelab and Why Is It Important?](https://stormagic.com/company/blog/what-is-homelab/)

So you can make a HomeLab with everything you havbe home, like an old pc or an potato-server.

![potato-server](potato-server.gif)

In my case I am thinging to buy/recicling:
- A low powered PC
- Some LARGE storage (SD? HDD?)
- Cables

At the time of the writing I don't buy anything for the project but I am planing to buy some things...

## What I want to run on it?

First thing: what I want to have as a service on my HomeLab?

- Feed reader: I read a lot of feed from the web
- Hosting for photo raw
- Tracking for books
- Tracking for anime/tv series/movies
- Tracking for manga
- Ad-Block for all the network
- An eBook manager library, if I can a software where can I add book on the fly with the WiFi, no cable
- Some home assistant/home automation

I thing this is all I need as a start. But searching online I found that it will be something problematic with only this stuff. I need to add more software/network tools.

![fire](fire.gif)

## So what I need to add?

- A domain name: real or not[^1]
[^1]: Real is a domain I bought, not real is a domain I create for my network without any real registry involved
- A local DNS for the domain
- A private Certificate Authority or automated reverse proxies for the local domain
- A tool for manage and deploy Docker or other type of container on the network
- A tool for backup
- A centralize authentication system for the app and the server/servers
- A dashboard as Home so I can go too every system
- A local documentation for personale use

If I not have all of this stuff the HomeLav will become something difficult to setup, mantain and manage.

![pc-trash](pc-trash.gif)

## So what now?

And now I am reasearching for the config, waiting for the parts, looking for the software and reading post and watching video about how to set up a HomeLab in my home (like where to put it). And I want to write more post about my homelab in the next future but it will be possible only when I have some hardware for build it. Ok I have some hardware for testing but I prefer to build it with the "final" hardware not the temp one.

The next post will be about how I set up all the things but It will not be a tutorial, it will be more like a diary about testing. At the end of all I will post some tutorial or, if I find something specific or something I find curiosus.
