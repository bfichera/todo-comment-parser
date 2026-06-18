import argparse
from pathlib import Path
from fnmatch import fnmatch

from .parser import Parser


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', type=str, default='TODO')
    parser.add_argument('--depth', type=int, default=None)
    parser.add_argument('--include', type=str, default=None)
    parser.add_argument('directory', type=Path)
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
                print(nondir.relative_to(root))
                parser.print()
