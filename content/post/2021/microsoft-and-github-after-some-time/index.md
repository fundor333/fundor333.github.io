---
title: "Microsoft and GitHub After Some Time"
date: 2021-08-07T14:03:16+02:00
feature_link: "https://unsplash.com/photos/cVMaxt672ss"
feature_text: "Photo by Liam Tucker on Unsplash"
tags:
- rant
slug: "Microsoft-and-GitHub-after-some-time"
categories: 
- rant
description: "Three years later I talk about Microsoft buying Github"
type: "post"
meta:
- github
- microsoft
---

This post is a follow up to one of my old post: [Microsoft buy Atom, Electron and Open Source](/post/2018/microsoft-buy-atom-electron-and-open-source).

## We start at the beginning

This story start with a tweet. I was scrolling on *Twitter* in June 2018 and I saw a retweet of this tweet.
{{< tweet jasonfried 430871267881672704 >}}

So I search more and find the [official blog's post](https://blogs.microsoft.com/blog/2018/06/04/microsoft-github-empowering-developers/) of the acquisition.

After reading it and some more research I write a [post](/post/2018/microsoft-buy-atom-electron-and-open-source).

## The big questions 

Now is three years after the original post and I have an answer for some of the questions i ask in my post. 

### Github has problems. Microsoft buying it will solve the problems or kill GitHub?

For what I know Microsoft solve most of the financial problem of Github, putting more money and reworking some aspects of the platform.

In the begining there was an _Exodus_ torward GitLab with _#movingtogitlab_ trending on twitter
{{< tweet gitlab 1004143715844124673 >}}

But with the new [GitHub Action](https://github.blog/2018-10-16-future-of-software/) Microsoft move a lot of user from Travis, CircleCi and GitLab CI. It is easier to use and you can find on GitHub a lot of pre-done action in the Marketplace.

And the year after with the [free privated repo](https://github.blog/2019-01-07-new-year-new-github/) Microsoft attack the marketpool of BitBucket and GitLab. A lot of the users of BitBucket and GitLab use them only for the free private repo so, if you have all the functions of GitLab and Bitbucket and the GitHub Action why someone need to stay on GitLab or BitBucket?

But the real nail on the coffin for the other platform was the [GitHub Sponsor](https://github.blog/2019-05-23-announcing-github-sponsors-a-new-way-to-contribute-to-open-source/). With this you can have your Patreon/Coffee/SponsorPlatform directly on your GitHub account or, if you want, connect with the existing sponsor site.

### The want to controll the OpenSource word or the only want to work with it?

Maybe they want more controll over Open Source. We had in the last three years more and more Microsoft projects on GitHub and they show old source code.

Because Microsoft is not a _Software Company_ anymore but more and more a _Software as a Service_ company with some _Hosting and Clouding_ related product they can share more and more code.

They also make more integration with the Microsoft Ecosystem.

### They want more contoll over Electron and his development?

I don't know. **NOW** they have more controll over the project. They want it? Maybe.
What I know is Microsoft is making more app with Electron (for now VSCode, Skype and Microsoft Team).

### They want to controll Atom development?

Microsoft kill Atom. This is how.

#### Add more integration for GitHub into VSCode

With some plugin and new functions in the core app, Microsoft add more support for GitHub into VSCode.
After this they add some of the exclusive feature of Atom to VSCode and the best integration ever: native sync of the VSCode's config and plugin with your GitHub/microsoft account.

#### Microsoft take away resource from Atom

Atom lost appeal after VSCode and Microsoft knows. I don't know if they remove resource because the lost appeal or because the don't want Atom but the [contributors](https://github.com/atom/atom/graphs/contributors)' tab on the GitHub page show a big decline in the Atom development.

#### They make an online editor _Codespace_

[Codespaces](https://github.com/features/codespaces) an online editor for git repository. Inside a codespace you can use any of the _Visual Studio Code Marketplace's Plugins_, a custom dotfiles and you can connect it to a VS Code. Strange they don't talk about Atom support in the Codespaces' page.

#### All the programming language has a plugin/collection

Microsoft, one at the time, implement a plugin/collection for language, with all the tool you need for the language. So VSCode support all language.

### They want to make more Azure into Github service and all the marketplace?

Now you have multiple integration from Azure to GitHub and from GitHub to Azure. And they add plugin into VSCode for debug or setting connection between your machine, GitHub and Azure.

## Conclusion

In my opinion is this[^1] bad for the Open Source community? 
[^1]: Microsoft owning GitHub
**_Yes_**. No one must controll the biggest hosting for code. 

_But how we can change the situation?_

We need a **_GitServer App Federated_** where you have only a piece of the all system.[^2]

[^2]: For example [Mastodon](https://docs.joinmastodon.org/) work in this way and they explain it in a easy way [here](https://youtu.be/IPSbNdBmWKE)

But if we don't have something _federated_ is better have all in one palce (GitHub) with backup than have all in distint server within GitLab/GiTea/Gogo Instance.

NB: this is my personal opinion.
