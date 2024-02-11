---
title: "Hugo With Lazy Loading and Webp"
date: 2021-07-27T10:00:00+02:00
feature_link: "https://unsplash.com/photos/9Gz5bMWdGYE"
feature_text: "Photo by Sara Julie on Unsplash"
tags:
- blog
- devops
- hugo
slug: "Hugo-with-lazy-loading-and-webp"
categories: 
- dev
- fingerfood
description: "Adding Lazy load, WebP and AVIF to your Hugo"
type: "post"
meta:
- webp
- avif
- lazy load
---

New work and new knowledge. For having a better site/blog performance you can use _loadding="static"_ in the resources you need last and, if there are img, you can use avif and webp for faster render page time.

So I need to implement into my personal Hugo's blog.

# Hugo problem

In Hugo you can edit the themplate for having all the "fix" img with lazy-loading or img alternative but if there are image inside a _.Content_of a post or other type you can't edit them in a easy way.
So I search online and found about the _/layouts/_default/_markup/render-image.html_ [^1].
[^1]: From [Hugo's Docs](https://gohugo.io/getting-started/configuration-markup/#markdown-render-hooks)

## A simple render-image

Render-image is an override of the default _markdown_ to _HTML_ with your custom code.
So I search for some example and this is the simple one:

``` go-html-template
<img loading="lazy" src="{{ .Destination | safeURL }}" alt="{{ .Text }}" {{ with .Title}} title="{{ . }}" {{ end }} />
```

So from

``` markdown
![Random img](cat.jpg)
```

we have

``` go-html-template
<img loading="lazy" src="cat.jpg" alt="Random img">
```

With only one line of code all the img inside a _.Content_ has an _alt_ filled and a _loading="lazy"_.

After this I want to add to all _img_ the _width_ and the _height_ of the image and, if present, add the [_WebP_](https://developers.google.com/speed/webp/) and/or [_AVIF_](https://aomediacodec.github.io/av1-avif/) for optimization (I suggest some article for more info [^2] [^3] [^4] [^5] )

[^2]: [Comparing AVIF vs WebP file sizes at the same DSSIM](https://www.ctrl.blog/entry/webp-avif-comparison.html)
[^3]: [On the hunt for the best image quality per byte](https://fronius.me/articles/2020-10-14-comparing-image-formats-jpg-webp-avif.html)
[^4]: [AVIF support](https://caniuse.com/avif)

[^5]: [WebP Compression Study](https://developers.google.com/speed/webp/docs/webp_study)

## Problems with Hugo's Statics File and Hugo's Page Bundles

I find some article about WebP and Hugo but there are some problems.
All the word who implement a solution for this problem has a blog without the [_Page Bundles_](https://gohugo.io/content-management/page-bundles/).

So I decide to choose one and "update" the solution for the _Page Bundles_. And my bas was this post: [WebP and AVIF images on a Hugo website](https://pawelgrzybek.com/webp-and-avif-images-on-a-hugo-website/).

### The code

So this is my final _render-image.html_.

``` go-html-template
{{- $src := ( .Destination | safeURL ) -}}
{{- if strings.HasPrefix $src "http" -}}
<img loading="lazy" src="{{ .Destination | safeURL }}" alt="{{ .Text }}" {{ with .Title}} title="{{ . }}" {{ end }} />
{{- else -}}
<picture>
  {{ $isJPG := eq (path.Ext .Destination) ".jpg" }}
  {{ $isPNG := eq (path.Ext .Destination) ".png" }}

  {{ if ($isJPG) -}}
  {{ $avifPath:= replace .Destination ".jpg" ".avif" }}
  {{ $avifPathStatic:= (add (add "/content/" .Page.Dir)  $avifPath) }}

  {{ if (fileExists $avifPathStatic) -}}
  <source srcset="{{ $avifPath | safeURL }}" type="image/avif">
  {{- end }}

  {{ $webpPath:= replace .Destination ".jpg" ".webp" }}
  {{ $webpPathStatic:= (add (add "/content/" .Page.Dir)  $webpPath )}}

  {{ if (fileExists $webpPathStatic) -}}
  <source srcset="{{ $webpPath | safeURL }}" type="image/webp">
  {{- end }}
  {{- end }}

  {{ if ($isPNG) -}}
  {{ $avifPath:= replace .Destination ".png" ".avif" }}
  {{ $avifPathStatic:= (add (add "/content/" .Page.Dir)  $avifPath )}}

  {{ if (fileExists $avifPathStatic) -}}
  <source srcset="{{ $avifPath | safeURL }}" type="image/avif">
  {{- end }}

  {{ $webpPath:= replace .Destination ".png" ".webp" }}
  {{ $webpPathStatic:= (add (add "/content/" .Page.Dir)  $webpPath )}}

  {{ if (fileExists $webpPathStatic) -}}
  <source srcset="{{ $webpPath | safeURL }}" type="image/webp">
  {{- end }}
  {{- end }}

  {{ $img := imageConfig (add (add "/content/" .Page.Dir)  .Destination) }}

  <img src="{{ .Destination | safeURL }}" alt="{{ .Text }}" loading="lazy" decoding="async" width="{{ $img.Width }}" height="{{ $img.Height }}" />
</picture>
{{- end -}}
```

The start if is for manage linked image and work as a base case of this code using the "simple" code for the base. 
For the "this is one of my blog's image" case we use a _picture_ tag. All the _source_ tags after are use only if ugo find the img with the correct img format.

But the real different form the _pawelgrzybek's code_. I get the image config form the image in the content and not from the static's path. With the config of the image we can get the width and the height of the img.

## That's all?

The only problem now is to make the WebP and the AVIF file from your image and _pawelgrzybek_ suggest this example for compressing the img:

``` bash
cwebp cat.jpg -o cat.webp
avifenc --min 10 --max 30 cat.jpg cat.avif
```

If you are a macOs user you can use [Homebrew](https://brew.sh/).

``` bash
brew install webp
brew install joedrago/repo/avifenc
```

If you add _webp_ and _avifenc_ to your build script like a [makefile]({{< ref "/post/2021/the-team-makefile" >}}) and integrate into your CI or your workflow.

If you need help or have some suggestion you can comment or [tweet me](https://twitter.com/fundor333)
