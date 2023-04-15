import pathlib
import re
import shutil
import subprocess
import tempfile

import markdown

from .post_install import post_install


_here = pathlib.Path(__file__).resolve().parent


def md_to_html(md):
    return markdown.markdown(
        md,
        extensions=["admonition", "pymdownx.superfences", "smarty"],
    )


def mkposter(datadir):
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
        bodies = contents.split("--split--")

        bodies = [md_to_html(b) for b in bodies]
        banner = bodies[0]

        html_out = "\n".join([f"""<!doctype html>
        <html>
        <head>
        <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,400i,700%7CRoboto+Mono&amp;display=fallback">
        <link rel="stylesheet" type="text/css" href="style.css"/>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        </head>
        <body>
        <div class="banner md-typeset">
        {banner}
        </div>
        <hr>
        <div class="body md-typeset">""",
        "\n".join([f"<div class=\"Coll{i}\">\n{body}\n</div>" for i, body in enumerate(bodies[1:])]),
        """
        </div>
        </body>
        </html>
        """])  # noqa: E501

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

        subprocess.run(["python", "-m", "http.server"], cwd=tempdir)
