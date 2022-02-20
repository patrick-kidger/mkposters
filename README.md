# Mkposters

Create your (academic) posters using Markdown.

The Markdown is parsed into HTML, styled using the (S)CSS from [mkdocs-material](https://github.com/squidfunk/mkdocs-material/), and then opened as a webpage, that you can then export to PDF.

## Installation

```
git clone https://github.com/patrick-kidger/mkposters
cd mkposters
pip install .
```

## Usage

#### Directory layout

```
somedir/
    foo/
        poster.md
        ...any other assets e.g. images...

somedir> python -m mkposters foo
```

#### Poster layout

`poster.md` should be formatted in three sections:

```
...anything you want appearing in the banner at the top...

--split--

...whatever you want in the left column...

--split--

...whatever you want in the right column...
```

Each section can/should be Markdown formatted.

#### Icons

Recalling that Markdown can embed HTML, then icons can be embedded via e.g.
```html
<img style="height: 20pt; width: 20pt" src="icons/fontawesome/brands/github.svg">
```
where the list of available icons is [here](https://github.com/patrick-kidger/mkposters/tree/main/mkposters/icons).

#### Mathematics

You can use LaTeX-formatted mathematics. This is done via

```
\\(inline math\\)
\\[display math\\]
```

Note the double backslash.

#### Admonitions

Admonitions can be added using the syntax

```markdown
!!! admonition_type "Your title here"

    Your text here
```

where `admonition_type` is any of [these](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#supported-types) types, e.g. `info`, `tip`, etc.

#### HTML

The Markdown format allows you use arbitrary HTML inside of it. This is useful in all kinds of ways.

- To make best use of this package you'll probably want to be proficient with HTML and CSS. You'll find that you're stuck with the default alignment on the webpage otherwise.
- This is particularly useful for the banner section, which often includes lots of pieces of information (titles, authors, logos, URLs, etc.) that you'll want to lay out in some manner.
- Pro tip: embedding HTML can be (ab)used to modify spacing like so. (Analogous to all those little `\vspace`s you use in LaTeX documents.) In this example we move the content up by 10 points.
```
<div style="margin-top: -10pt;">
...your content here...
</div>
```
