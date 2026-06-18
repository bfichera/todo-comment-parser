import argparse
from pathlib import Path
from fnmatch import fnmatch
from warnings import warn

from .parser import Parser


def rgb(text, r, g, b):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', type=str, default='TODO')
    parser.add_argument('--depth', type=int, default=None)
    parser.add_argument('--include', type=str, default=None)
    parser.add_argument('directory', nargs='?', type=Path, default=Path.cwd())
    cfg = parser.parse_args()

    root = cfg.directory
    tag = cfg.tag
    max_depth = cfg.depth
    include = cfg.include

    start_depth = len(root.parts)
    for top, dirs, nondirs in root.walk():
        depth = len(top.parts) - start_depth
        if max_depth is not None:
            if depth > max_depth:
                continue
        for nondir in [top / nd for nd in nondirs]:
            if include is not None:
                if not fnmatch(nondir.name, include):
                    continue
            parser = Parser.from_file(nondir, tag)
            if parser is not None:
                try:
                    if parser.todo_pars:
                        print(rgb(nondir.relative_to(root), 255, 0, 0))
                        parser.print()
                except ValueError as e:
                    warn(e)
