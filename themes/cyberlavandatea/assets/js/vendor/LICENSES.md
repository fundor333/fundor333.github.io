# Vendored third-party scripts

These files are bundled so the theme has no required runtime CDN dependency.
They are unmodified upstream builds.

| File | Library | Version | License |
|------|---------|---------|---------|
| `lunr.min.js` | [Lunr.js](https://lunrjs.com/) | 2.3.9 | MIT |
| `purify.min.js` | [DOMPurify](https://github.com/cure53/DOMPurify) | 3.2.6 | Apache-2.0 OR MPL-2.0 |
| `webmention.min.js` | [webmention.js](https://github.com/PlaidWeb/webmention.js) | — | MIT (Expat) |

Font Awesome and KaTeX are **not** vendored: they are optional (Font Awesome
only for the content-type icons, KaTeX only when `math` is set) and large, so
they load from a CDN / Kit and are configurable. Google Fonts (Audiowide /
Rajdhani) are loaded from `fonts.googleapis.com` and configurable via
`params.fonts`; a site can self-host them instead.
