import sys

from .mkposter import mkposter


_, filename = sys.argv
mkposter(filename)
