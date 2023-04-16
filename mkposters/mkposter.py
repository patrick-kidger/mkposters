import os
import pathlib
import re
import shutil
import subprocess
import tempfile
import time

import markdown

from .post_install import post_install


_here = pathlib.Path(__file__).resolve().parent


def md_to_html(md: str):
    return markdown.markdown(
        md,
        extensions=["admonition", "pymdownx.superfences", "smarty"],
    )


def exclude_hidden_dirs(path, subdirs):
    return [p for p in subdirs if p.startswith(".")]

def parse(datadir: pathlib.Path, tempdir: pathlib.Path, join_scss_file: pathlib.Path):
    if (datadir / "icons").exists():
        raise ValueError
    if (datadir / "stylesheets").exists():
        raise ValueError
    shutil.copytree(datadir, tempdir, dirs_exist_ok=True, ignore=exclude_hidden_dirs)

    md_file = tempdir / "poster.md"
    html_file = tempdir / "index.html"
    css_file = tempdir / "style.css"

    with md_file.open() as f:
        contents = f.read()
    bodies = contents.split("--split--")

    bodies = [md_to_html(b) for b in bodies]
    banner = bodies[0]
    left_body = bodies[1]# Still capture left and right seperatly for backwards compadibility
    right_body = bodies[-1]
    
    html_out = "\n".join([rf"""<!doctype html>
    <html>
    <head>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,400i,700%7CRoboto+Mono&amp;display=fallback">
    <link rel="stylesheet" type="text/css" href="style.css"/>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script type="text/javascript" src="https://livejs.com/live.js"></script>
    </head>
    <body>
    <div class="banner md-typeset">
    {banner}
    </div>
    <hr>
    <div class="body md-typeset">
    <div class="left">
    {left_body}
    </div>""", 
    *[f"<div class=\"Middle_{i}\">\n{body}\n</div>" for i, body in enumerate(bodies[2:-1])],
    rf"""<div class="right">
    {right_body}
    </div>
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
            str(join_scss_file),
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


def max_file_time(path: pathlib.Path):
    times = []

    for subpath in path.iterdir():
        if not subpath.match(".*"):
            if subpath.is_file():
                times.append(subpath.stat().st_mtime)
            elif subpath.is_dir() and list(subpath.iterdir()):
                times.append(max_file_time(subpath))

    return max(times)


def main(datadir):
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = pathlib.Path(tempdir)
        datadir = pathlib.Path(datadir)
        (tempdir / "style.scss").touch()  # default
        join_scss_file = tempdir / "join_style.scss"
        shutil.copyfile(_here / "join_style.scss", join_scss_file)
        shutil.copyfile(_here / "custom.scss", tempdir / "custom.scss")
        (tempdir / "stylesheets").symlink_to(
            _here / "third_party" / "stylesheets", target_is_directory=True
        )
        (tempdir / "icons").symlink_to(
            _here / "third_party" / "icons", target_is_directory=True
        )
        file_time = max_file_time(datadir)
        need_update = True
        process = None
        try:
            while True:
                if need_update:
                    last_time = file_time
                    parse(datadir, tempdir, join_scss_file)
                    if process is None:
                        print("Starting")
                    else:
                        print("Detected change; reloading")
                        process.kill()
                    process = subprocess.Popen(["python", "-m", "http.server"], cwd=tempdir)
                time.sleep(0.1)  # check every tenth of a second
                file_time = max_file_time(datadir)
                need_update = file_time > last_time
        finally:
            if process is not None:
                process.kill()
