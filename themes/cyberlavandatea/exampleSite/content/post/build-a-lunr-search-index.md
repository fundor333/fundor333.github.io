+++
title = "Build a search index with Lunr in Hugo"
date = 2026-09-08T10:00:00+02:00
description = "A custom output format that emits search.json, queried client-side with Lunr."
tags = ["hugo", "search", "javascript"]
categories = ["dev"]
toc = true
isStarred = true
+++

Hugo can emit a **custom output format**: a `search.json` file with every page.
The client downloads the index once and then queries
[lunr](https://lunrjs.com/) locally.

## The index template

```js
// build the index from the rendered pages
const index = lunr(function () {
  this.ref("uri");
  this.field("title");
  this.field("content");
  for (const doc of request.response) {
    this.add(doc);
    lookup[doc.uri] = doc;
  }
  return 200;
});
```

> Note: the index is rebuilt on every build. With a few hundred posts the file
> stays under 200&nbsp;KB.

Results are rendered from a `<template>` cloned per match, with the same summary
truncation Hugo itself uses.
