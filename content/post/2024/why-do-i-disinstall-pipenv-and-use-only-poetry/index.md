---
title: "Why Do I Disinstall Pipenv and Use Only Poetry?"
date: 2024-07-10T11:34:15+01:00
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

Some time ago I wrote about my preference to write Terminal Commands for what I need [^1] and thant was not the end of it.
[^1]: [Why I Stop Making Script and Start to Make Bash Terminal Commands]({{< ref "/post/2023/why-i-stop-making-script-and-start-to-make-bash-terminal-commands" >}} "Why I Stop Making Script and Start to Make Bash Terminal Commands")

~~Sometime~~ More than often I need to build the same basic structure for code a Terminal Command and I usualy use a _makefile_[^2] for the building of the project or the command specific for this particolar project[^makefile].

[^2]: [The team makefile]({{< ref "/post/2021/the-team-makefile" >}} "The team makefile")
[^makefile]: [How to create a self-documenting Makefile](https://victoria.dev/blog/how-to-create-a-self-documenting-makefile/)

But I don't like to repeate the same thing over and over so I develop with git and pyproject a "blank" project as template for my personal python project (there is also a Django Blank Template but I use it less and less).

The main idea of the template is to build something with all I need for python, not only the "booring stuff" but also some cool stuff like automation.
I toke some ispiration from other post and project of mine [^dotfile] [^gitops] for the base of the template.

[^gitops]: [From DevOps to GitOps]({{< ref "/post/2021/from-devops-to-gitops" >}} "From DevOps to GitOps")

[^dotfile]: [Dotfiles, bot and yaml files]({{< ref "/post/2020/dotfiles-bot-yaml" >}} "Dotfiles, bot and yaml files")

![VEnv](venv.png)

## Starting the .venv

If you are coding in Python you must use a _virtual env_ for easy dev and testing so I search for tools.

I love the __.venv__ and all the cleaner workspace which came with it but I choose, at the begginning, the wrong tool for automation of the _venv_.

In the beginning, I wrote all my project with a _pipfile_[^3] in mind which is a good idea for a deploy, not for a package.

[^3]: [Pipenv e come tutto è in uno]({{< ref "/post/2017/pipenv-e-come-tutto-e-in-uno" >}} "Pipenv e come tutto è in uno")

If it is a personal project you need to run only on your machine and not relese anyware else it is a great tool because Pipenv is build for deploy only. 

But with the new white hairs on my head I change my mind.

If I want to become something bigger than a little dev I find usefull have all the code and the test ready for mass distribuition or having a simpler system to install on a pc or server as a command like a _Click_ program. 
So I search more and find pyproject and I want to try it.

But PyProject without a tool is horrible, no other words... 
It's easy to read but you need to know all the parameters and keywords for editing or updating soo... No, I don't like it, but maybe there are some tools for edit pyproject in a easy way so I search for something more funtional and easy to use and _poetry_ was suggested to me. [^poetry-over-pipenv]

[^poetry-over-pipenv]: Beautifull article about Poetry over others [I move from pipenv to poetry in 2023 - Am I right ?](https://dev.to/farcellier/i-migrate-to-poetry-in-2023-am-i-right--115)

### Poetry

Poetry is a terminal tool for creating and manipolation of _venv_ and _pyproject.toml_'s files.
With some expirience I add more stuff in the _pyproject_ for the basic.

One the best thing of _poetry_ is the clean way you can edit the settings of the project and build, clean and upgrade your venv.

PS: usually I have the _.venv_ inside the project thanks to this command

```bash
poetry config --local virtualenvs.in-project true
```

### Editor config

With poetry we have the _venv_ so now we need to define the style of the code and check if the code is following it.

So I find [Editor config](https://editorconfig.org/), one of the best thing I found on the web. 

It is a tool split in two part:
1. A config file (.editorconfig) with the indication for all the type of the file of the project and how they must be formatted[^editorconfig]
2. A checker (something implemented in an IDE, an IDE Plugin, CI) which format or check the code following the .editorconfig file configuration.

[^editorconfig]:I have a multifile format file done by me but if you need to start you can generate your own [here](https://editorconfig.timseverien.com/) 

In my case every time I save something the editor (VSCode in my case) will reformatting the code following the .editorconfig settings.

I feel the need for this tool because I worked with some developer who wrote _Spaghetti Code_ every day so or I kill him or I use this tool...

![Spaghetti code](spaghetti-code.png)

### Pre-Commit

This is something I use as safety net for myself. Some time I work at night or with time restriction I make error or make something not python-like but spaghetti-like and this is bad, very bad.

For this reason I add _pre-commit_[^pre-commit] for autofix and check all this minor error. 
And because I add _pre-commit_ I add more dotfiles for configurations of all the parts of the project and the tools for make more check and fix some of the problems.

[^pre-commit]: [Using pre-commit hooks to write better code](https://praful932.dev/blog-2-pre-commit-hooks/)

If you set pre-commit in the right way for your project, you have an automatic way to make your local machine check your code and valitated the new code without pushing and "waysting" CI cycles [^waysting] and fix the problems before the CI say "Wrong, wrong, wrong, wrong, You are WRONG".

![Worng](wrong.gif)

[^waysting]: Sometime you have a slow CI or a "premium" CI so the cycles are a fine resource to keep.

## Conclusion

This is the consempt for a generic python project but you can do it for all the type of projects and make your personal [templating repo of Github](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) and add other stuff, for example a blank template for Kubernates with some type of checker of the config (maybe with _pre-commit_).

You can also expand the idea adding some _dotfile_ for the IDE, like the config for running the project with multiple setting (dev mod, presentation, online, staging) or the default config four your prefer CI tool.
