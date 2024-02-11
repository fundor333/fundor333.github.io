---
title: "Why Do I Disinstall Pipenv and Use Only Poetry?"
date: 2024-01-25T21:57:15+01:00
draft: true
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
tags:
- poetry
- pipenv
- pyproject
- pyenv
slug: "why-do-i-disinstall-pipenv-and-use-only-poetry"
categories:
- dev
- coding
description: "I choose to don't use pipenv and move to poetry and pyproject and other stuff for dev with python"
type: "post"
mp-syndicate-to:
- https://brid.gy/publish/twitter
- https://brid.gy/publish/mastodon
images:
keywords:
---
Some time ago I wrote about my preference to write Terminal Commands for what I need [^1] and thant was not all.
{^1]: [Why I Stop Making Script and Start to Make Bash Terminal Commands]({{< ref "post/2023/why-i-stop-making-script-and-start-to-make-bash-terminal-commands" >}} "Why I Stop Making Script and Start to Make Bash Terminal Commands")

~~Sometime~~ More than often I need to build the same basic project for make a Terminal Command and I usualy use _makefile_[^2] for the building of the project or the command specific for this or that particolar project[^makefile].

[^2]: [The team makefile]({{< ref "/post/2021/the-team-makefile" >}} "The team makefile")
[^makefile]: [How to create a self-documenting Makefile](https://victoria.dev/blog/how-to-create-a-self-documenting-makefile/)

So I develop with git and pyproject a "blank" project as template for my personal python project.

The main idea is to build something with all I need for python, not only the "booring stuff". 
I toke some ispiration from other post and project of mine [^dotfile] [^gitops]
[^gitops]: [From DevOps to GitOps]({{< ref "/post/2021/from-devops-to-gitops" >}} "From DevOps to GitOps")

[^dotfile]: [Dotfiles, bot and yaml files]({{< ref "/post/2020/dotfiles-bot-yaml" >}} "Dotfiles, bot and yaml files")

![VEnv](venv.png)

## Starting the .venv

I love the __.venv__ and all the cleaner workspace which came with it but I choose, at the begginning, the wrong tool.

In the beginning, I wrote all my project with a _pipfile_[^3] in mind.

[^3]: [Pipenv e come tutto è in uno]({{< ref "/post/2017/pipenv-e-come-tutto-e-in-uno" >}} "Pipenv e come tutto è in uno")

If it is a personal project you need to run only on your machine and not relese anyware else it is a great tool. But with the new white hairs I change my mind.

I find usefull have all ready for mass distribuition of some of my code or having a simpler system to install as a command one script made in _Click_ and, because pyproject will be the new standard, I try it.

PyProject without a tool is horrible. It's easy to read butyou need to know all the parameters and keywords soo...

And I need others tools which are inside dedicate dotfiles so I search for something more funtional and easy to use and _poetry_ was suggested to me.

### Poetry

Poetry is a terminal tool for creating and manipolation of _venv_ and _pyproject.toml_'s files.
With some expirience I add more stuff in the _pyproject_ for the basic.

### Pre-Commit and Editor-config

Some time I work at night or with time restriction I make error or make something not python-like but spaghetti-like and this is bad.
![Spaghetti code](spaghetti-code.png)

For this reason I add _pre-commit_[^pre-commit] and _editorconfig_ for autofix all this minor error. And because I add _pre-commit_ I add more dotfiles for configurations of all the parts of the project and the tools.

[^pre-commit]: [Using pre-commit hooks to write better code](https://praful932.dev/blog-2-pre-commit-hooks/)









**Update** 
[Here]({{< ref "/post/2024/why-do-i-disinstall-pipenv-and-use-only-poetry" >}} "Here") you can find some update about the way I write code and my personal utility
