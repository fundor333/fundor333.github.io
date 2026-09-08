+++
title = "Costruire un indice di ricerca con Lunr in Hugo"
date = 2026-09-08T10:00:00+02:00
description = "Un output format personalizzato per generare search.json e interrogarlo con Lunr lato client."
tags = ["hugo", "search", "javascript"]
categories = ["dev"]
toc = true
isStarred = true
+++

Hugo può generare un **output format personalizzato**: un file `search.json` con
tutte le pagine. Il client scarica l'indice una sola volta e poi interroga
[lunr](https://lunrjs.com/) in locale.

## Il template dell'indice

```js
// costruisce l'indice a partire dalle pagine renderizzate
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

> Nota: l'indice va rigenerato a ogni build. Con qualche centinaio di post il
> file resta sotto i 200&nbsp;KB.

Il rendering dei risultati usa un `<template>` clonato per ogni match, con lo
stesso troncamento del sommario che fa Hugo.
