import pathlib

import mkposters


_here = pathlib.Path(__file__).resolve().parent


def test_example():
    diffrax_example = _here.parent / "examples" / "diffrax"
    mkposters.mkposter(diffrax_example, timeout_s=1)
