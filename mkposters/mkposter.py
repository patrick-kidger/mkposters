import pathlib
import re
import shutil
import subprocess
import tempfile

import markdown


_here = pathlib.Path(__file__).resolve().parent


def md_to_html(md):
    return markdown.markdown(
        md,
        extensions=["admonition", "pymdownx.superfences"],
    )


def mkposter(datadir):
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = pathlib.Path(tempdir)
        datadir = pathlib.Path(datadir)
        shutil.copytree(datadir, tempdir, dirs_exist_ok=True)
        (tempdir / "icons").symlink_to(_here / "icons", target_is_directory=True)

        md_file = tempdir / "poster.md"
        html_file = tempdir / (md_file.stem + ".html")
        style_file = tempdir / "style.css"

        with md_file.open() as f:
            contents = f.read()
        banner, left_body, right_body = contents.split("--split--")

        banner = md_to_html(banner)
        left_body = md_to_html(left_body)
        right_body = md_to_html(right_body)
        out = rf"""<!doctype html>
        <html>
        <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,400i,700%7CRoboto+Mono&amp;display=fallback">
        <link rel="stylesheet" type="text/css" href="style.css"/>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        </head>
        <body>
        <div class="banner md-typeset" align="center">
        {banner}
        </div>
        <hr>
        <div class="body md-typeset">
        <div class="left">
        {left_body}
        </div>
        <div class="right">
        {right_body}
        </div>
        </div>
        </body>
        </html>
        """  # noqa: E501

        subprocess.run(
            [
                f"{_here}/dart-sass/sass",
                f"{_here}/stylesheets/main.scss",
                str(style_file),
                "--no-source-map",
            ]
        )
        with style_file.open() as f:
            contents = f.read()
        style_pieces = []
        svg_load = re.compile(r"""svg-load\(["']([\w\.\-/]+)["']\)""")
        while (match := svg_load.search(contents)) is not None:
            (filename,) = match.groups()
            start, end = match.span()
            style_pieces.append(contents[:start])
            style_pieces.append("url('data:image/svg+xml;charset=utf-8,")
            with pathlib.Path(_here / "icons" / filename).open() as f:
                style_pieces.append(f.read())
            style_pieces.append("')")
            contents = contents[end:]
        style_pieces.append(contents)

        with style_file.open("w") as f:
            f.write("".join(style_pieces))
        with html_file.open("w") as f:
            f.write(out)

        subprocess.run(["python", "-m", "http.server"], cwd=str(tempdir))
