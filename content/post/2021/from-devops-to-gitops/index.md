---
title: "From DevOps to GitOps"
date: 2021-10-08T12:46:23+02:00
feature_link: "https://unsplash.com/photos/I7A_pHLcQK8"
feature_text: "Photo by Mae Mu on Unsplash"
tags:
- dotfiles
- devops
- gitops
slug: "From-DevOps-to-GitOps"
categories: 
- dev
description: "Why am I moving from DevOps to GitOps"
type: "post"
meta:
- google
- kubernetes
- git
- github
- github action
- hacking
- ansible
---

## Introduction

In this blog I wrote a lot about automation and devops[^1] and now I am studying _GitOps_.
[^1]: [Here some articles](http://localhost:1313/tags/devops/)

## What is GitOps?

_GitOps_ is an evolution of _DevOps_.

> DevOps is a set of practices that combines software development and IT Operations.
> It aims to shorten the systems development life cycle and provide continuous delivery with high software quality
>
> Wikipedia

Usually this is done with script and automation (tools, code, ape with a keyboard...) and remove some human error.

_DevOps_ is a deployment practices, in other way is a philosophy. 
In any way you have a concept without an implementation. 

_DevOps_ define a way of working and we need something more practical for the world.

With _DevOps_ in mind we can make an implementation of this set of steps:

* _Coding_ writing code 
* _Building code_ automatic build or similar application specific
* _Testing code_ in automatic way and you don't have bug on the deploy
* _Approving_ with issue and merge requests
* _Packaging_ code read for production
* _Releasing_ the deploy of the software
* _Configuring_ the software and all the other stuffs
* _Monitoring_ check if the software crash, use all the rams, eat some people...

And write an _microservice_'s app or deploy your blog while sleeping become the new day to day life.

_GitOps_ decide to create a _Universal model_ for develop and maintain an _It infrastructure_. The main idea is _Infrastructure as Code_ and put all is software and configs into a Git repo.

This Idea has an huge example into Kubernetes where all is a _Yaml file_ and must be committed somewhere.

## This is a new think?

In this blog there are some articles about dot-files and other *gitops* stuffs bifore there sere called GitOps.

You can make script, automations and configs into a file and make it deplora with the DevOps’s technique.

You must also have testing and deploy within a _git_ repo. So you must use stuff like GitHub Action or TravisCI for testing and automations.

## Do I need to have Kubernetes?

No, you don't. You can use all sort of automations. You can write your own tools or you can use something like Kubernetes, Ansible, etc...

The main focus is to have a good Git server (GitHub, GitLab,GitTea,...) for hosting your repo and automation for apply the code and the config into your infrastructure.

## Why do I gain from using it?
First of all you *gain time*. If you have an history of all your change in the infrastructure you can roll back in an easy way (revert a commit) and you can add test for the config and other stuff like router configurations.

Second you have a *way to approve* the changes *before* something crash in a bad way.

Third this is a really easy way to replicate a server or a configuration or edit it in a cluster of machine without logging inside all the machine or launch command after command. You only need to change the config/code in the repos and push to the master/main/deploy branch.

Forth you can have one or more Manager/Supervisor watching and approving all the changes (with the pull requests and fixes) and approving or deny them *before* something become a problem or a huge problem.

## My team is one or two dev/devops/sysadmin/ttech guy...

If you don't have man power you *need* to use this technique for trying to have more work within the same time with the same check or even more.

## I can use it for my little project?

Yes, you can. This blog is a _GitOps_ example. 

This site is made with all the necessary stuff and the configs inside repos. 

All you need for run it is inside one of two repo:

* A repo with the source code of the blog (img, HTML, CSS, posts, etc...)
* The Hugo repo (the software for building my blog)

### An Example
In this repos (the blog one) you have 

#### The Data

Like the posts and the images used in this blog and all the info for the Search engine are store in plain files. Some of them are media file but a lot of them are text files (a lot of _MarkDown_ files and some _Json_). Only the comments are outside of the repo.

#### The Code
All the template and the Css/JavaScript of the site (and in my case the SCSS for building the Css). 
I also have a couple script for generating compressed img for the web.[^2] 
[^2]: [Hugo With Lazy Loading and Webp]({{< relref "post/2021/Hugo-with-lazy-loading-and-webp" >}}) 


#### The Config
An the _config folder_ where is define some stuff for build the site like the menu or the meta needed for the compression or CoockieLaw.
It also have some config for GitHub for the GitHub Action and the config for GitHub Pages.

#### The Testing
I added some GitHub Action for building the site and test for 404 or similar error after the build. In this way I don't need to check all the link manually.

#### Console/command file
I need this for dev and run it because I don't remember all the commands. In my case an easy to use _makefile_ with some command for building, cleaning and testing the site before deploy it on the _world wild web_.[^3] 
[^3]: [The team Makefile]({{< relref "post/2021/the-team-makefile" >}}) 

## Conclusion

Working in a little team _GitOps_ is an essential tool for our teamwork. 
Good luck for your implementation of _GitOps_
