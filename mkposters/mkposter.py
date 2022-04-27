import pathlib
import re
import shutil
import subprocess
import tempfile

import markdown
from pymdownx.superfences import fence_div_format

from .post_install import post_install


_here = pathlib.Path(__file__).resolve().parent


def md_to_html(md):
    return markdown.markdown(
        md,
        extensions=["admonition", "pymdownx.superfences", "smarty"],
        extension_configs={
            "pymdownx.superfences": {
                "custom_fences": [
                    {"name": "mermaid", "class": "mermaid", "format": fence_div_format}
                ]
            }
        },
    )


def mkposter(
    datadir: str,
    code_style: str = "github",
    background_color: str = "#FFFFFF",
    port: int = 8000,
):
    """
    Make a poster from a Markdown file.
    Args:
        datadir (str): The directory containing the Markdown file.
        code_style (str): The style of code blocks.
        background_color (str): The background color of the poster.
        port (int): The port to use for the server.
    Returns:
        Rendered markdown as HTML via `http.server` on specified port.
    Example:
        ```bash
        python -m mkposters "research_app/poster" --code_style "github" --background_color "#F6F6EF" --port 8000
        ```
    """

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = pathlib.Path(tempdir)
        datadir = pathlib.Path(datadir)
        shutil.copytree(datadir, tempdir, dirs_exist_ok=True)
        (tempdir / "icons").symlink_to(
            _here / "third_party" / "icons", target_is_directory=True
        )

        md_file = tempdir / "poster.md"
        html_file = tempdir / (md_file.stem + ".html")
        css_file = tempdir / "style.css"

        with md_file.open() as f:
            contents = f.read()
        banner, left_body, right_body = contents.split("--split--")

        banner = md_to_html(banner)
        left_body = md_to_html(left_body)
        right_body = md_to_html(right_body)
        html_out = rf"""<!doctype html>
        <html>
        <head>
        <body style="background-color:{background_color}">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,400i,700%7CRoboto+Mono&amp;display=fallback">
        <link rel="stylesheet" type="text/css" href="style.css"/>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/{code_style}.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js"></script>
        <script>hljs.initHighlightingOnLoad();</script>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.css">
        <script src="https://unpkg.com/mermaid@9.0.1/dist/mermaid.min.js"></script>
        <script>mermaid.initialize();</script>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        </head>
        <body>
        <div class="banner md-typeset">
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

        # check if post-install of dart-sass is needed
        if not (_here / "third_party" / "dart-sass" / "SASSBUILT.txt").exists():
            post_install(package_dir=str(_here))

        subprocess.run(
            [
                f"{_here}/third_party/dart-sass/sass",
                f"{_here}/style.scss",
                str(css_file),
                "--no-source-map",
            ]
        )
        with css_file.open() as f:
            css_out = f.read()

        def svg_load_fn(match):
            (filename,) = match.groups()
            with pathlib.Path(_here / "third_party" / "icons" / filename).open() as f:
                contents = f.read()
                return f"url('data:image/svg+xml;charset=utf-8,{contents}')"

        svg_load_re = re.compile(r"""svg-load\(["']([\w\.\-/]+)["']\)""")
        css_out = svg_load_re.sub(svg_load_fn, css_out)

        with css_file.open("w") as f:
            f.write(css_out)
        with html_file.open("w") as f:
            f.write(html_out)

        serve_cmd = f"python -m http.server {port}"
        subprocess.run(serve_cmd.split(" "), cwd=tempdir)
