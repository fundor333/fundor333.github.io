---
title: 'Why Do I Disinstall Poetry and Use Only Uv '
date: 2026-01-26 21:58:02+01:00
feature_link: https://www.midjourney.com/home/
feature_text: by IA Midjourney
description: null
isStarred: false
tags:
- poetry
- pipenv
- pyproject
- pyenv
- uv
- makefile
- make
- precommit
categories:
- dev
- fingerfood
images: null
keywords: null
series:
- Python's Reptile Env
syndication:
- https://mastodon.social/@fundor333/115963459189684445
comments:
  host: mastodon.social
  username: fundor333
  id: '115963459189684445'
---

558 days ago (yes I count them), I wrote a follow-up article called [Why Do I Disinstall Pipenv and Use Only Poetry?](/post/2024/why-do-i-disinstall-pipenv-and-use-only-poetry/) and now I remake mine dev space, for building python project.

Some of the arguments are old, some are new but all come from my dev stack.

## Build a .venv

For every Python project I wrote, I code all the project with a Virtual Env or .venv.
It is a local "installation" of Python for the folder and it keep all the dependency inside it.

It is the best way to develop python project because you can have any number of Python project, with different version of Python and/or different version of the dipendency for each project.

Because I use git I need a good way to lock and commit the dipendency of my project. Some time ago I was using Poetry but now I use UV for build, update and manage the Virtual Env

![virtual-environment-make.jpg](virtual-environment-make.jpg)

## Creating a .env file

Every python project I create, I always add a .env file, where I store all the environment variable for the project but I don't add them to the repo because It is not necessary add the local config for dev in a repo.

You can also automatically use the .env file in Uv so every time you are inside the .venv, you also have all the variables.

## Using UV

So after some time I was using Poetry and Pipenv, I find [UV](https://github.com/astral-sh/uv), a tool write in Rust for locking dipendnecy, set up and manage the .venv and create package for the publication in one tool.

You can easly start a procjet with a simple command

{{<highlight bash>}}
uv init
{{</highlight >}}

which create the pyproject.toml and the .venv with all the dipendency.

With some other command you can easily add, remove and update the dipendency or import in a easy way your .env file.

{{<highlight bash>}}
uv run --env-file=.env
{{</highlight >}}

I move to UV because I can use a single tool for all my python necessity and it is faster and less bugged.

## Editor Config

We have the .venv, we have the .env, we have the dependency manager so I add the Editor Config file for the style of the code.
The [Editor Config file](https://editorconfig.org/) is a file where you define the style for the type of file you write in your repo.

I have mine made year after year but I start with the [example](https://editorconfig.org/#example-file) in the site because it is easy and with all the stuff you need.

## Makefile it

So, after adding stuff over stuff to the repo, I add a makefile where yu have all the aliases for a python project, [^1].

[^1]: I wrote an article about makefile caller [The Team Makefile](https://fundor333.com/post/2021/the-team-makefile/)

My basic makefile is something like this

{{<highlight Makefile>}}
SHELL := /bin/bash

RUNNER := uv run --env-file=.env

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Make venv and install requirements
	@uv sync
	@$(RUNNER) pre-commit install
	@pre-commit autoupdate

.PHONY: update
update: ## Update requirements
	@uv lock --upgrade
	@$(RUNNER) pre-commit autoupdate

precommit: ## Run pre-commit hooks
	@git add . & uv run --env-file=.env pre-commit run --all-files
{{</highlight >}}

The help command come form a blog post[^2] and describe better at my other post[^3]

[^2]: [How to create a self-documenting Makefile](https://victoria.dev/archive/how-to-create-a-self-documenting-makefile/)
[^3]: [The Team Makefile](https://fundor333.com/post/2021/the-team-makefile/)

I write a makefile for all my project because I forgot a lot of the command and parameters, so a makefile is a good way to have an "deploy" command or a "test" command for the project and forgot all the task needed for run a "test" or a "deploy".

I also put all the test command into the makefile because sometime the test command is too long to remember...

## Pre commit and some automation

This is my personal safety net for the commits. Some time I wrote and push without any work or thing about what I am doing... For this reason I add pre-commit[^pre-commit] for autofix and check all this minor error.

[^pre-commit]: [Using pre-commit hooks to write better code](https://praful932.dev/blog-2-pre-commit-hooks/)

![cox.gif](cox.gif)

The took launch a lot of test BEFORE I can save the commit so I can find the error or getting a big fat NOPE for the commit, which I need to review for the problem.

## Conclusion

This is the stack I work with and I love it. It can be something custom and old style for some of the older tecnology but I find it complete for what I do.
