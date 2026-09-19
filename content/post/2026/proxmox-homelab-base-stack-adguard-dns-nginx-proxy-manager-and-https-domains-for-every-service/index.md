---
title: "Proxmox Homelab Base Stack: AdGuard DNS, Nginx Proxy Manager, and HTTPS Domains for Every Service"
date: 2026-09-19 14:54:53+02:00
draft: true
feature_link: https://matteoscarpa.it/
feature_text: by Fundor333/Matteo Scarpa/Me
description: null
isStarred: false
tags:
- homelab
- proxmox
- nginx
- adguard
- nginx-proxy-manager
- adguard-dns
categories:
- tinkering
series:
- My Home Automation Lab
---

And after some searching and some buying (and some exchange with sombody I know) I built my HomeLab core/main server.[^1]

[^1]: Searching for a name for the server. If you have one comment this post with it thanks.

"It" is
- ZimaBoard2 [^2]
- 2 WD Red Plus Internal NAS HDD 3.5 4 TB[^3]

I set the HDD in Raid1 for replication and I install ProxMox VE as OS[^4]. The installation software for the distro make the RAID1 for my HDDs.

[^2]: Suggestion from a friend to have it as a main server. [ZimaBoard2](https://www.zimaspace.com/it/products/single-board2-server) will be the main server and controller for the all system (for now)
[^3]: This specific HDD are for NAS or Server soo... I take what I can buy [link](https://www.westerndigital.com//products/internal-drives/wd-red-plus-sata-3-5-hdd?sku=WD40EFZZ)
[^4]: [ProxMox VE](https://pve.proxmox.com/wiki/Main_Page) is a Debian (❤️‍🔥) base distribution for manage virtualization.

![homelab.jpg](homelab.jpg)

After some problem (I only have the TV as monitor and I don't have very long cable) I had a working HomeLab for start.

## The start

I

![1495 from xkcd](hard_reboot.png)
