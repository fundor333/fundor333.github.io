# Changelog

All notable changes to this theme are documented here.
The format is loosely based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- Initial release of **CyberLavandaTea**: a dark-only Hugo theme for dev/code
  blogs, built with Tailwind CSS v4.
- 6-role palette (one violet, one green) defined once in `assets/css/main.css`
  `@theme`; the full layout in plain CSS with Tailwind utility fallbacks.
- Layouts: `baseof`, `home`, `list` (grouped by year), `single`, `404`,
  `taxonomy`, `term`; section layouts for `micro`, `photos` (EXIF table),
  `weeknote`, `event`, `now`, `series`, `search`.
- `<head>`: meta, Open Graph, Twitter cards, JSON-LD `BlogPosting`, canonical,
  `hreflang`, pagination `rel` links.
- Feeds: RSS, Atom (`feedUUID`, `webfeeds`), JSON Feed 1.1, `humans.txt`,
  dynamic `robots.txt`; client-side search via a `SearchIndex` output format and
  Lunr.
- IndieWeb / POSSE: Microformats2 markup, Webmention (send + render), Mastodon
  comments, build-time toot embed, Brid.gy Publish markup, syndication list.
- "Also posted on" syndication labels are prettified per platform at build
  time: `reddit.com/r/django/…` shows **r/django**, `bsky.app/profile/x` shows
  **@x**, `…/@user/…` shows **host/@user**; other links show the host.
- Render hooks: link (UTM + new tab + marker), image (`<figure>` + caption),
  heading (anchor), codeblock (`HighlightCodeBlock`).
- Shortcodes: `toc`, `embed`, `toot`, `xkcd`, `allpages`, `88x31`, `buzzword`,
  `heart`.
- Content-type icons via Font Awesome (Kit or free CDN), `params.postIcons`
  override.
- Footer: 88×31 badges, webring partial (icon / prev-next / web component),
  "cite this post", "written by a human", backlinks, related posts.
- Opt-in LGBTQ+ corner (pride.codes), `params.prideCorner` (default `false`).
- Favicons rendered entirely from config (`_partials/favicons.html`):
  `favicon`, `faviconSvg`, `appleTouchIcon`, `icon96`, `webmanifest`,
  `maskIcon`; falls back to the theme's bundled `favicon.svg`.
- Webmention rendering: `#webmentions` facepile + inline comments are now
  styled in `main.css`; `_partials/webmention.html` keeps the URL scheme when
  swapping the host and takes `script` / `wordcount` params.
- Mastodon comments (`_partials/mastodon.html`): full auto-loading reply thread
  from `<host>/api/v1/statuses/<id>/context` — avatars, instance badges,
  localised dates, favourites count, OP marker, custom emoji, DOMPurify — from
  `comments = { host, username, id }` front matter. Styled by `section#comments`.
- i18n: `en` and `it`.
- `exampleSite` that builds cleanly on Hugo 0.146+.
