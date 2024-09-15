---
title: "New Render Image For Hugo"
date: 2024-07-28T11:37:47+02:00
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
tags:
- blog
- devops
- hugo
- module
slug: "new-render-image-for-hugo"
categories:
- dev
- fingerfood
description: "The new way to elaborate image for the site generation of the site with Hugo Module"
type: "post"
mp-syndicate-to:
- https://brid.gy/publish/twitter
- https://brid.gy/publish/mastodon
images:
keywords:
aliases:
- "/post/2024/new-render-image-fot-hugo/"
---

## The story so far

Some time ago I wrote a post about _lazy loading_ and _WebP_ in _Hugo_ [^1] and how I implemented it.
[^1]: Fundor333 - [Hugo With Lazy Loading and Webp](/post/2021/hugo-with-lazy-loading-and-webp/)

When you add image in your Hugo's site you also launch some script for some image optimization.
Some problems come from the custom script for the build, were you need to have other code install in your machine or wherever you compile your static site.

It was a good implementation and a fast one but some time after I find a better way to implement better way to serve img in a static site, so I wrote a new article [^2] where I describe the implementation with a "Hugo's way" with a internal pipeline.

[^2]: Fundor333 - [Generate WebP and AVIF with Hugo](/post/2021/webp-and-avif-with-hugo-generator/)

In this implementation I combine as find in a blog post [^5] the _srv_ html tag [^src-tag] in the _picture_ tag [^picture-tag] without the Avif format file[^avif]

[^src-tag]: Mozilla wiki - [Src set](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/srcset)
[^picture-tag]: Mozilla wiki - [Tag HTML picture](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture)
[^5]: From Bennett Notes - [Hugo Responsive Images With Markdown Render Hook](https://www.bennettnotes.com/notesnotes/hugo-responsive-images-with-markdown-render-hook/)
[^avif]: GitHub issue - [Add image processing support for AVIF](https://github.com/gohugoio/hugo/issues/7837)

I don't like this way because it is inside the theme. I want to have this function like something I can import in any of my Hugo projects without copy and pasting the same code any time.

So I search for something like a package for Hugo so I find the [Hugo Module](https://gohugo.io/hugo-modules/)


## GoHugo Module

_Hugo_ is write in _GoLang_ so the dev implement a way to use a _golang module_ as add-on for your _Hugo_ site.

In my module [Macia Image](https://github.com/fundor333/macia-image)[^maciaImage] I implemented a 'partial theme' which the only think it does is optimize the image of the posts like the one done for the second post [^2]

[^maciaImage]: _Macia_ (like the tea) is the name of all my Hugo's module and _Image_ for the scope of the project


### Code

So this is my code form the path _**layouts/_default/_markup/render-image.html**_ in the theme from the old way [^2] but now it is at the new path of the module _**layouts/_default/_markup/render-image.html**_ where I build the images **INSIDE** the post.

```     go-html-template

{{/* Original code from: https://laurakalbag.com/processing-responsive-images-with-hugo/   */}}
{{/* Just modified a bit to work with render_image hook and output webp images   */}}
{{/* get file that matches the filename as specified as src=""  */}}
{{ $src := .Page.Resources.GetMatch (printf "%s" (.Destination | safeURL))  }}
{{ $alt := .PlainText | safeHTML }}

{{/* So for posts that aren't setup in the page bundles, it doesn't fail  */}}
{{ if $src }}

{{ $format := cond (eq $src.MediaType.SubType "gif") "" "webp" -}}

{{ $xs := .Page.Site.Params.maciaimage.tiny }}
{{ $s := .Page.Site.Params.maciaimage.small }}
{{ $m := .Page.Site.Params.maciaimage.medium }}
{{ $l := .Page.Site.Params.maciaimage.large }}

{{ $tinyw := default (printf "%s %s" $xs $format) }}
{{ $smallw := default (printf "%s %s" $s $format) }}
{{ $mediumw := default (printf "%s %s" $m $format) }}
{{ $largew := default (printf "%s %s" $l $format) }}

{{/* resize the src image to the given sizes */}}
{{/* We create a a temp scratch because it`s not available in this context */}}
{{ $data := newScratch }}

{{ $data.Set "tiny" ($src.Resize $tinyw) }}
{{ $data.Set "small" ($src.Resize $smallw) }}
{{ $data.Set "medium" ($src.Resize $mediumw) }}
{{ $data.Set "large" ($src.Resize $largew) }}

{{/* add the processed images to the scratch */}}

{{ $tiny := $data.Get "tiny" }}
{{ $small := $data.Get "small" }}
{{ $medium := $data.Get "medium" }}
{{ $large := $data.Get "large" }}

{{/* only use images smaller than or equal to the src (original) image size, as Hugo will upscale small images */}}


<a href="{{ $src.RelPermalink }}">
    <picture>

      <source media="(max-width: 376px)"
          srcset="{{with $tiny.RelPermalink }}{{.}}{{ end }}">

      <source media="(max-width: 992px)"
          srcset="{{with $small.RelPermalink }}{{.}}{{ end }}">

      <source media="(max-width: 1400px)"
          srcset="{{with $medium.RelPermalink }}{{.}}{{ end }}">

      <source media="(min-width: 1600px)"
          srcset="{{with $large.RelPermalink }}{{.}}{{ end }}">

      <img alt="{{ $alt }}" title="{{ $alt }}" src="{{ $src }}" loading="lazy" decoding="async" height="{{ $src.Height}}" width="{{ $src.Width }}" class="{{.Page.Site.Params.maciaimage.imgclass}}">

    </picture>
</a>

  {{/* Since I do image-response class, the only thing that really
  matters is the height and width matches the image aspect ratio */}}

  {{ end }}

```   

In this code I set some values from the configs of the site so you can customize it in your theme and import it when ever you need it.

## NB

This code, unlike the old one [^2], support the _Gif_ file format and output only file as _WebP_ and a lot of them.
As you can see in the script, the code generate 4 copy of the original image with 4 different image size (configurable in the config of the site).

When the Hugo's Team add support for _Avif_[^5] I will add it into the module for generate all the image with the config setting which format image will be outputting.
