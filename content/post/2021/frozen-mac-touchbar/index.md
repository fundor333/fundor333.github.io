---
title: "Frozen Mac Touchbar"
date: 2021-12-10T21:28:14+01:00
feature_link: "https://unsplash.com/photos/4mX4kRRubIw"
feature_text: "Photo by Sumudu Mohottige on Unsplash"
tags:
- hacking
- rant
slug: "frozen-mac-touchbar"
categories: 
- fingerfood
- dev
description: "Sometime you need to fix your frozen Mac TouchBar"

meta:
- mac
- repair
- touchbar
---

## The touchbar

Sometime you need to do some task. If you have a MacBook Pro you can have a touchbar. Sometime *Works* sometime *Freezes*. And it freezes in the most Murphy's way[^1] possible.
[^1]: [Murphy's law](https://en.wikipedia.org/wiki/Murphy%27s_law) *Anything that can possibly go wrong, does*
Something like googling "mac touch bar not working" or "mac touch bar freezes"

In my personal experience it stops when play a *bad* song on Spotify.

### What's happened?

Your *touch bar* can be in one of this three state:

1. _A working *touch bar*_ which is the natural state of the Mac
2. _A frozen *touch bar*_ which is a crashed state of the *touch bar* of the Mac
3. _A blank *touch bar*_ which is my favourite state of the *touch bar* of the Mac

So can I fix it? Yes!

## Fixing it

An *user logout* sometime fix the problem. Sometime not allways will fix it.
*Restart* the Mac will allways fix the problem but sometime you can't restart the machine for a _minor_ fix so you need something else for the fix. Something like a command.

### Bash for the win

If you need to _restart_ the *touch bar* without restarting your Mac you can use this bash fragment.

``` bash
sudo pkill TouchBarServer;
sudo killall "ControlStrip";
```
Your welcome
