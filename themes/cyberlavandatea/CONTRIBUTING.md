# Contributing to CyberLavandaTea

Thanks for taking the time to help.

## Ground rules

- **English only** for code, comments, commit messages, docs and issues.
- The theme is **dark-only** on purpose — please don't add a light mode.
- The palette is six roles plus two derived surfaces. New colours in the site
  *chrome* are out of scope; syntax highlighting may use the two documented
  tints and the single error red, and nothing else.
- Keep the layout working **without** Tailwind's content detection: put real
  styling in `assets/css/main.css` (`@layer base` / `@layer components` / plain
  rules), not only in template class attributes.

## Local development

```bash
npm install
npm --prefix exampleSite install
hugo server -s exampleSite --themesDir ../..
```

Or, module-style:

```bash
cd exampleSite
hugo mod get -u
hugo server
```

## Before opening a PR

- `hugo --source exampleSite --themesDir ../.. --environment production` builds
  with no errors and no new deprecation warnings.
- Add an entry to `CHANGELOG.md` under `## [Unreleased]`.
- If you touched params or front matter, update `README.md`.

## Releasing (maintainers)

Tag with a SemVer tag (`vX.Y.Z`). Hugo Modules resolve theme versions from Git
tags, so a tag is all that's needed to publish a new version.
