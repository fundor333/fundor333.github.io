---
title: "WebP and Avif With Hugo's Static Site Generator"
date: 2021-11-04T09:02:45+01:00
feature_link: "https://unsplash.com/photos/eO11kAf7G7U"
feature_text: "Photo by ikhsana baihaqi on Unsplash"
tags:
- hugo
- devops
slug: "WebP-and-Avif-with-Hugo-generator"
categories:
- fingerfood
- dev
description: "Generate WebP and AVIF with Hugo"
meta:
- webp
- avif
- lazy load
- microformat
series:
- Hugo tricks
---

## In the last episode

Some time ago I wrote about Hugo, WebP, AVIF and the lazy loading[^1].
[^1]: [Hugo with lazy loading and webp]({{< ref "/post/2021/hugo-with-lazy-loading-and-webp/index.md" >}})

In the main time I read more about it and find more about the Hugo's render hook and the picture and img tag[^2] [^3].

[^2]: [Src set](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/srcset)
[^3]: [Tag HTML picture](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture)

I did like this way because I don't find a "elegant solution" for the Avif/WebP generation problem.
I don't like my way of generating Avif/WebP with a code outsite the Hugo pipeline like my old post[^1] or my ispiration[^p].
[^p]: [WebP and AVIF images on a Hugo website](https://pawelgrzybek.com/webp-and-avif-images-on-a-hugo-website/)

I need a *better way to do it*.

And one day I recive an issiue[^4] on Github about an implementation with more responsive implementation[^5] (and more clean).
[^4]: [THE ISSIUE](https://github.com/fundor333/fundor333-source/issues/116)
[^5]: [Hugo Responsive Images With Markdown Render Hook](https://www.bennettnotes.com/notes/hugo-responsive-images-with-markdown-render-hook/)

So I rewrote all the render hook.

1. I will make the WebP image

2. Put the code for the AVIF[^pp] because now Hugo don't support AVIF

[^pp]: [Add image processing support for AVIF](https://github.com/gohugoio/hugo/issues/7837)

3. Add support for multiple img size

## The code

So this is my code form the path _**layouts/_default/_markup/render-image.html**_ where I build the images **INSIDE** the post.

```     go-html-template

{{ $src :=  .Page.Resources.GetMatch (printf "%s" (.Destination | safeURL)) }}
{{ if $src }}

<picture>
    <!-- AVIF -->

    {{ $tinyw := default "500x avif" }}
    {{ $smallw := default "800x avif" }}
    {{ $mediumw := default "1200x avif" }}
    {{ $largew := default "1500x avif" }}

    {{ $data := newScratch }}
    {{ $data.Set "tiny" ($src.Resize $tinyw) }}
    {{ $data.Set "small" ($src.Resize $smallw) }}
    {{ $data.Set "medium" ($src.Resize $mediumw) }}
    {{ $data.Set "large" ($src.Resize $largew) }}

    {{ $tiny := $data.Get "tiny" }}
    {{ $small := $data.Get "small" }}
    {{ $medium := $data.Get "medium" }}
    {{ $large := $data.Get "large" }}

    <source media="(max-width: 376px)"
        srcset="{{with $tiny.RelPermalink }}{{.}}{{ end }}">

    <source media="(max-width: 992px)"
        srcset="{{with $small.RelPermalink }}{{.}}{{ end }}">

    <source media="(max-width: 1400px)"
        srcset="{{with $medium.RelPermalink }}{{.}}{{ end }}">

    <source media="(min-width: 1600px)"
        srcset="{{with $large.RelPermalink }}{{.}}{{ end }}">

    <!-- WebP -->

    {{ $tinyw := default "500x webp" }}
    {{ $smallw := default "800x webp" }}
    {{ $mediumw := default "1200x webp" }}
    {{ $largew := default "1500x webp" }}

    {{ $data := newScratch }}
    {{ $data.Set "tiny" ($src.Resize $tinyw) }}
    {{ $data.Set "small" ($src.Resize $smallw) }}
    {{ $data.Set "medium" ($src.Resize $mediumw) }}
    {{ $data.Set "large" ($src.Resize $largew) }}

    {{ $tiny := $data.Get "tiny" }}
    {{ $small := $data.Get "small" }}
    {{ $medium := $data.Get "medium" }}
    {{ $large := $data.Get "large" }}

    <source media="(max-width: 376px)"
        srcset="{{with $tiny.RelPermalink }}{{.}}{{ end }}">

    <source media="(max-width: 992px)"
        srcset="{{with $small.RelPermalink }}{{.}}{{ end }}">

    <source media="(max-width: 1400px)"
        srcset="{{with $medium.RelPermalink }}{{.}}{{ end }}">

    <source media="(min-width: 1600px)"
        srcset="{{with $large.RelPermalink }}{{.}}{{ end }}">


  <img class="img-post u-photo" src="{{ .Destination | safeURL }}" alt="{{ .Text }}" loading="lazy" decoding="async" width="{{ $src.Width }}" height="{{ $src.Height }}" />
</picture>
{{end}}

```

In this code I mix some of code of my old post, some of else code and some of new code.

And when the Hugo team will implement the AVIF we will be ready for it.

## Conclusion

This magic code will be easy to read and has:

1. WebP Support
2. AVIF Support
3. Loading Lazy
4. Image size support
5. MicroFormat support

So it is Internet ready and easy to forget and you can write a good post with all the optimization done for you.
