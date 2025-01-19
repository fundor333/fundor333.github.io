---
title: "My Zsh Command History"
date: 2025-01-17T11:47:42+01:00
description: "And I print my ZSH History"
isStarred: false
tags:
- dev
- zsh
categories:
- dev
images:
keywords:
- bash
- terminal
- zsh
series:
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
---

For social pression of some blogger I follow ([Andrea Grandi](https://www.andreagrandi.it/posts/my-zsh-history/),[Nicola Iarocci](https://nicolaiarocci.com/my-most-used-command-line-commands/), [Chris DeLuca](https://www.chrisdeluca.me/2024/12/31/my-cli-wrapped-most-used.html) ) I follow with the history of my terminal (ZSH)

- 90 git
- 49
- 38 open
- 34 poetry
- 27 make
- 26 hugo
- 26 brew
- 24 cd
- 18 npm
- 14 pipenv

As a dev the first command is _git_... The second command is a bad habits I have... Spam new line in the terminal...
I don't find _ls_ and I find it strange...

Here the command I used

``` bash
history | awk '{print $1}' | sort | uniq --count | sort --numeric-sort --reverse | head -10
```
