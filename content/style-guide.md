---
title: "Style Guide"
type: page
specialpost: true
allpage: true
summary: A listing of all the styles and elements used on this site
---

Inspired by [json.blog's style guide](https://json.blog/style-guide/) and, in turn, [The Frugal Gamer](https://www.thefrugalgamer.net/styleGuide.php), a (not so[^notso]) comprehensive listing of all possible styles and elements on this site.

[^notso]: Actually, this is also not comprehensive. If you find I forgot something ping me and I will fix it

# Heading 1

## Heading 2

### Heading 3

#### Heading 4

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

### In-line styles

**Bilbo Baggins:** Good morning!

**Gandalf:** ( *leaning on his staff* ) What do you mean? Do you wish me a good morning, or mean that it is a good morning whether I want it or not; or that you feel good this morning; or that it is a morning to be good on?

This is a [link](https://en.wikipedia.org/wiki/The_Hobbit).

You can also write some `inline code` when you need it.

### Block Styles

#### Quote

> "I wish it need not have happened in my time," said Frodo. "So do I," said Gandalf, "and so do all who live to see such times. But that is not for them to decide. All we have to decide is what to do with the time that is given us."

#### Alert Boxes

> **Note** — Notes are for supplementary information the reader might find useful but can skip without losing the main point.

> **Tip** — Tips suggest a better way to do something or a shortcut worth knowing.

> **Important** — Important alerts highlight information that is critical to the reader's understanding or success.

> **Warning** — Warnings flag something that could cause problems if ignored — proceed carefully.

> **Caution** — Caution signals a potentially irreversible or destructive action.

#### Tables

I don't really use tables much, but here's one anyway.

| Column 1  |  Column 2  | Column Blue |
| :-------- | :--------: | ----------: |
| Left Text |  Centered  |       22.50 |

#### Code

Code is also rare on the blog, though it's a big part of my "day life". Here's a bit of Python.

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

These are the colors featured on this site's theme.

| Role       | Light     | Dark      |
| :--------- | :-------- | :-------- |
| Accent     | `#003fff` | `#77a8fd` |
| Code text  | `#f8f8f2` | `#f8f8f2` |
| Code back  | `#272822` | `#272822` |
| Table rule | `#dadada` | `#717171` |
