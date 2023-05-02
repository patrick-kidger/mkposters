<h1 align="center">MkPosters</h1>

Create posters using Markdown. Supports icons, admonitions, and LaTeX mathematics.

At the moment it is restricted to the specific layout of two-columns-with-banner-at-the-top, as that's what I tend to use. (Pull requests are welcome if you want to make this tool more general.) The poster can be either portrait or landscape.

The library operates by parsing your Markdown into HTML, styling it with CSS, and then opening a webpage that you can export to PDF.

## Example

<img style="height: 400pt; width: auto;" src="https://raw.githubusercontent.com/patrick-kidger/mkposters/main/imgs/diffrax.png" alt="Example poster">

The "source code" for this example is [here](https://github.com/patrick-kidger/mkposters/tree/main/examples/diffrax).

## Assumptions

Assumes you have:
- Linux (WSL is fine) or macOS
- Firefox
- Python

Compatibility with other operating systems is probably possible by switching out the version of Dart Sass being used internally.  
Compatibility with other browsers is unlikely.

You'll need to be relatively familiar with HTML and (S)CSS to make best use of MkPosters.

## Installation

```
pip install mkposters
```

## Usage instructions

1. Create the appropriate directory structure

```
foo/
    poster.md
    style.{css,scss} (optional)
    ...any other assets e.g. images...
```

2. Lay out your poster

`poster.md` should be formatted in three sections, with a literal "`--split--`" between each section.

```
...whatever you want in the banner at the top...

--split--

...whatever you want in the left column...

--split--

...whatever you want in the right column...
```

3. Build poster

Run from the directory containing `foo`:
```
bash> python -m mkposters foo
```

(The first time you do this MkPosters will attempt to automatically detect system architecture and install the appropriate required build of `dart-sass`. This was tested working on both an Apple M1 and Ubuntu x86_64 machine.) This will also automatically watch the `foo` directory for any updates.

4. View poster

Now open Firefox (*not* Chrome etc.) and navigate to `localhost:8000`.

What you see will be based on the size of your current browser window and may differ from the PDF version. So next hit `Control-P` and select "Save to PDF". What you see in the print preview is what you'll actually end up with!

Make all your edits until you're happy with the result. Now let's save the result to PDF.

5. Save to PDF

Saving to PDF can be quite finickity, and in general depends on choice of browser etc. (For what it's worth the following is tested using Firefox on Windows 10 with `mkposters` running on Ubuntu 20.04 on WSL2.)

In the print dialog window we opened above:
- Destination: "Save to PDF". **Do not use "Microsoft Print to PDF".**
- Orientation: (portrait or landscape, as desired)
- Pages: Custom: 1
- Paper size: (whatever is desired; current styling works best on paper roughly A4 sized)
- Margins: None
- Options: uncheck "Print headers and footers"

**Once again, make sure you're using Firefox.** Using other browsers (e.g. Chrome) or other PDF exporters (e.g. WeasyPrint) can introduce a variety of issues, such as saving text as images (which are unselectable in the PDF, and appear slightly pixelated), missing parts of the styling, or having faded colours (looking at you, Chrome).

## Functionality

MkPosters comes with a few extra pieces of functionality built in.

#### Icons

Recalling that Markdown can embed HTML, then icons can be embedded via e.g.
```html
<img style="height: 20pt; width: 20pt" src="icons/fontawesome/brands/github.svg">
```
where the list of available icons is [here](https://github.com/patrick-kidger/mkposters/tree/main/mkposters/third_party/icons).

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

### Custom (S)CSS styling

If you want to style your poster in a custom way, then you can include a `style.css` or `style.scss` file in your poster directory.

#### HTML

The Markdown format allows you use arbitrary HTML inside of it.

- The banner section often contains information (titles, authors, logos, URLs etc.) laid out in complicated ways. Directly writing HTML with embedded `style` attributes is simplest here. [See the start of this example.](https://raw.githubusercontent.com/patrick-kidger/mkposters/main/examples/diffrax/poster.md)
- HTML can be (ab)used to modify spacing like so. (Analogous to those little `\vspace`s you definitely never use in LaTeX documents.) In this example we move the content up by 10 points.
```
<div style="margin-top: -10pt;">
...your content here...
</div>
```

## Future plans?

It'd be nice to support:
- Other poster layouts, e.g. multiple columns;
- Optionally automatically generating the PDF. (Practically speaking probably by automating the Firefox interaction through Selenium.)
- Reducing package size by not including all of the `mkposters/third_party/icons` directory by default?

Pull requests welcome! See [CONTRIBUTING.md](https://github.com/patrick-kidger/mkposters/blob/main/CONTRIBUTING.md).

## Similar tools

These all support some kind of conversion Markdown -> something.
- For documentation: [MkDocs](https://github.com/mkdocs/mkdocs/) with [mkdocs-material](https://github.com/squidfunk/mkdocs-material/).
- For presentations: [reveal.js](https://github.com/hakimel/reveal.js)
- For static sites: [Hugo](https://github.com/gohugoio/hugo) or [Jekyll](https://github.com/jekyll/jekyll)
