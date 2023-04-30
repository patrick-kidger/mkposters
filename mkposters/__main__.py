import sys

from ._mkposter import mkposter


_, filename = sys.argv
mkposter(filename)
