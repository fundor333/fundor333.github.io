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
- Render hooks: link (UTM + new tab + marker), image (`<figure>` + caption),
  heading (anchor), codeblock (`HighlightCodeBlock`).
- Shortcodes: `toc`, `embed`, `toot`, `xkcd`, `allpages`, `88x31`, `buzzword`,
  `heart`.
- Content-type icons via Font Awesome (Kit or free CDN), `params.postIcons`
  override.
- Footer: 88×31 badges, webring partial (icon / prev-next / web component),
  "cite this post", "written by a human", backlinks, related posts.
- Opt-in LGBTQ+ corner (pride.codes), `params.prideCorner` (default `false`).
- i18n: `en` and `it`.
- `exampleSite` that builds cleanly on Hugo 0.146+.
