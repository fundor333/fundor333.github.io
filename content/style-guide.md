---
title: "Style Guide"
type: page
allpage: true
summary: A listing of all the styles and elements used on this site
---

Inspired by [json.blog's style guide](https://json.blog/style-guide/) and, in turn, [The Frugal Gamer](https://www.thefrugalgamer.net/styleGuide.php), a (not so[^notso]) comprehensive listing of all possible styles and elements on this site.

The site runs the **CyberLavandaTea** theme (v1.3.1): dark only, two accent hues (a green and a blue), display headings in *Audiowide*, body text in *Rajdhani*.

[^notso]: Actually, this is also not comprehensive. If you find I forgot something ping me and I will fix it

# Heading 1

The display face at its largest. Each heading level has its own voice, not just a smaller size, so the hierarchy reads at a glance.

## Heading 2

Still the display face, one step down, with a hairline underneath and a short green segment at its start. Inside a post it opens a section, so it also works as a divider.

### Heading 3

Switches to the body face, bold, in green: a sub-section title that stands out from the paragraph without competing with the h2 above it.

#### Heading 4

A mono, uppercase, letter-spaced label in grey, prefixed with a green `//`, like a comment tag in a config file.

Headings get an `id` and, on hover, a `¶` anchor link to that section.

And now, for the text content, which is the most important part of the blog.

## Content

### Paragraphs

In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort. It had a perfectly round door like a porthole, painted green, with a shiny yellow brass knob in the exact middle. The door opened on to a tube-shaped hall like a tunnel: a very comfortable tunnel without smoke, with panelled walls, and floors tiled and carpeted, provided with polished chairs, and lots and lots of pegs for hats and coats — the hobbit was fond of visitors. The tunnel wound on and on, going fairly but not quite straight into the side of the hill — The Hill, as all the people for many miles round called it — and many little round doors opened out of it, first on one side and then on another. No going upstairs for the hobbit: bedrooms, bathrooms, cellars, pantries (lots of these), wardrobes (he had whole rooms devoted to clothes), kitchens, dining-rooms, all were on the same floor, and indeed on the same passage.

### Lists

- Unordered List 1
- Unordered List 2
  - Nested list 1
  - Nested list 2

1. Ordered List 1
2. Ordered List 2

List markers look like CLI output, not book-style bullets: a green `▸` for unordered lists and zero-padded indices (`01`, `02`…) for ordered ones, both in the mono face.

### Footnotes

Footnote references[^fn] use the same treatment as ordered lists: a green, mono, zero-padded number. So the `01` in the text matches the `01` in the footnote list at the bottom of the page.

[^fn]: The footnote list is an `<ol>` too, so it gets the same markers as every other numbered list.

### In-line styles

**Bilbo Baggins:** Good morning!

**Gandalf:** ( *leaning on his staff* ) What do you mean? Do you wish me a good morning, or mean that it is a good morning whether I want it or not; or that you feel good this morning; or that it is a morning to be good on?

This is a [link](https://en.wikipedia.org/wiki/The_Hobbit).

You can also write some `inline code` when you need it.

### Links

Links are blue. A [visited link](https://en.wikipedia.org/wiki/The_Hobbit) turns sage green, and on hover every link goes green. External links open in a new tab and get a `↗` marker.

### Images

A block image is centered inside a `<figure>`; the title, if present, becomes the caption.

![A cup of tea](/img/logo.png "This title line renders as the caption")

To center a raw `<img>` outside a figure, add the `center-img` class.

### Block Styles

#### Quote

> "I wish it need not have happened in my time," said Frodo. "So do I," said Gandalf, "and so do all who live to see such times. But that is not for them to decide. All we have to decide is what to do with the time that is given us."

Blockquotes have a green left border on a slightly lifted surface. There are no separate "note / warning / caution" callout boxes — a quote is a quote.

#### Tables

I don't really use tables much, but here's one anyway. Rows alternate with a faint tint and the whole thing sits inside a scroll container when it's too wide.

| Column 1  |  Column 2  | Column Blue |
| :-------- | :--------: | ----------: |
| Left Text |  Centered  |       22.50 |

#### Code

Code is also rare on the blog, though it's a big part of my "day life". Here's a bit of Python. Syntax highlighting stays inside the two accent hues: keywords are green, strings blue, function names a lighter blue, numbers a lighter green, comments grey.

```python
from pathlib import Path


def read_calibration(file_path: str) -> list[str]:
    return Path(file_path).read_text().splitlines()


def find_numbers(line: str) -> list[str]:
    return [char for char in line if char.isdigit()]


def combine_first_and_last(numbers: list[str]) -> str:
    if not numbers:
        return "0"
    return numbers[0] + numbers[-1]


def sum_lines(lines: list[str]) -> int:
    return sum(int(line) for line in lines)
```

### Color Guide

The theme is dark only. Six semantic roles, plus surfaces derived from Content by opacity — nothing else in the site chrome.

| Role                | Token                 | Hex       |
| :------------------ | :-------------------- | :-------- |
| Primary (green)     | `--color-primary`     | `#5FD88F` |
| Content             | `--color-content`     | `#E6E6EC` |
| Links (blue)        | `--color-link`        | `#4D9FFF` |
| Visited (sage)      | `--color-visited`     | `#7EA88E` |
| Background          | `--color-background`  | `#14151A` |
| Inactive            | `--color-inactive`    | `#8B8F9A` |
| Surface (derived)   | `--color-surface`     | `#25262B` |
| Border (derived)    | `--color-border`      | `#313237` |
| Surface hover (derived) | `--color-surface-2` | `#2D2E33` |

Syntax highlighting palette:

| Token                     | Hex       |
| :------------------------ | :-------- |
| keyword / operator        | `#5FD88F` |
| string                    | `#4D9FFF` |
| function / class          | `#A8C9FF` |
| number / constant         | `#8FE0AF` |
| comment                   | `#8B8F9A` |
| error / removed line      | `#FF6F6F` |

Type:

| Use                                        | Family                                  |
| :----------------------------------------- | :-------------------------------------- |
| h1, h2, links, bold, footer                | Audiowide                               |
| Body text, h3                              | Rajdhani                                |
| Code, list markers, footnote refs, h4      | mono stack (SF Mono / JetBrains Mono…)  |
| "Written by a human" signature             | Ocean Trace                             |
