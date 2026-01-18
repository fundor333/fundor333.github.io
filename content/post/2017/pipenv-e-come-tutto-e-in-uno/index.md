---
title: Pipenv and all in one tool
slug: pipenv-e-come-tutto-e-in-uno
date: 2017-07-01 00:00:00 +0000
lastmod: 2025-01-18T23:10:15+01:00
categories:
- dev
tags:
- python
- dev
- pipenv
aliases:
- "/dev/pipenv-e-come-tutto-e-in-uno/"
description: Witnessing the marriage of Pipfile, Pip, and Pipenv.
feature_link: "https://unsplash.com/photos/vYFcHzLYpmU"
feature_text: "Photo by Max Letek on Unsplash"
series:
- Python's Reptile Env
---

> ⚠️ This post is obsolete. ⚠️
> 
> I suggest to go to the newest post from the [Python's Reptile Env series](/series/pythons-reptile-env/)

I am a big fan of podcasts. I enjoy listening to them while I'm commuting or at the gym. One of my favorites is by [Kenneth Reitz](https://www.kennethreitz.org/), the author of several Python modules, including *Requests*, which every Pythonista knows and uses.
His latest project that caught my interest is PipEnv, the *"sacred marriage of pipfile, pip, and virtualenv."*

Let’s start with the basics: to create a Python project, you usually go through 3 mandatory phases:

* You create a *virtualenv* to work in, so that installed packages don't conflict with those in the system, providing a clean environment.
* You select the modules needed for the project and install them in the *virtualenv* using *pip*.
* You generate a *requirements.txt* file from the *virtualenv* that indicates what is installed.

This requires you to constantly keep the *virtualenv* updated and clean, keep the *requirements.txt* file synchronized, and pin the minimum versions (or the exact version) of the modules in the *requirements.txt*.

PipEnv does all of this for you with a few simple commands.

## For example?

Let’s say I need to create a Python script that fetches RSS feeds and saves them locally.

* I create a folder for the project to keep everything I need organized:

``` bash
  mkdir python_project
```


* I choose which Python version to use, whether the current one or the *legacy* version:
``` bash
  pipenv --three # current Python 3.x version
  # alternatively
  pipenv --two # legacy 2.7.x

```


* I start writing code and installing the necessary packages for the project:

``` bash
  pipenv install requests
  pipenv install flask

```



These commands, along with the initial setup, allow me to create a *Pipfile* that describes the modules I've installed. The best thing about this *Pipfile* is that it allows for multiple "environments" within the same file. This means I can have "testing", "travis", "dev", and "prod" all described in a single file and managed automatically.

Now, suppose I realize I no longer need *flask* because I’ve rewritten everything to make the code more readable without it... What do I do?

``` bash
    pipenv uninstall flask

```

This command removes flask from the *Pipfile*, keeping it "clean" and always up to date.

Once the *Pipfile* is defined, you need to create the *Pipfile.lock*—an automatically generated version based on the "current installation" to perfectly reproduce the environment.

``` bash
    pipenv lock

```

This pins the installed modules with their version, hash, and other data for both the specified packages and their dependencies, providing all the information needed to reproduce that exact environment.

## Is that all?

No, the system initially creates a *virtualenv* for the project and populates it according to the terminal commands.
This virtual environment is accessible via the command:

``` bash
    pipenv shell
```

This opens a shell within the project's *virtualenv* and allows you to execute commands inside that specific environment.

Furthermore, *PipEnv* allows you to convert existing *requirements.txt* files into a *Pipfile* if they are not already present, and to update all packages using:

``` bash
    pipenv update
```

## Conclusion

Personally, I hope this system—or at least the *Pipfile*—becomes the standard for Python application development and replaces *requirements.txt* files, which I find particularly impractical and too sparse, even if they do exactly what they were designed for.
