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

`posters.md` should be formatted in three sections:

```
...anything you want appearing in the banner at the top...

--split--

...whatever you want in the left column...

--split--

...whatever you want in the right column...
```

Each section can/should be Markdown formatted.

#### Icons

Recalling that Markdown can embed HTML; icons can be embedded via e.g.
```
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
