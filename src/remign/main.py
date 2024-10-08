from __future__ import annotations

import functools
import os
import shutil
import sys
import typing

from .types_ import MatcherFunctionType
from .utils import make_matchers, match_matchers, parse_opts

if typing.TYPE_CHECKING:
    from collections.abc import Iterable, Sequence


def get_paths(matchers: Sequence[MatcherFunctionType], top: str) -> Iterable[str]:
    """Returns iterable of paths that match the patters given in ignore file."""

    matches = functools.partial(match_matchers, matchers=matchers)

    for path, dirs, filenames in os.walk(top):
        joiner = functools.partial(os.path.join, path)

        for dir_ in dirs:
            dir_path = joiner(dir_)
            if matches(dir_path):
                yield dir_path
            else:
                paths_iter = map(joiner, filenames)
                match_iter = filter(matches, paths_iter)
                yield from match_iter


def delete_paths(paths: Iterable[str]) -> None:
    """Deletes each path in given paths."""

    for path in paths:
        # it is already deleted
        if not os.path.exists(path):
            continue
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def main() -> None:
    options = parse_opts()
    if len(sys.argv) == 1:
        if not os.path.exists(options.files[0]):
            print("No `.gitignore` found in current directory.", file=sys.stderr)
            return
    matchers = make_matchers(options.files)
    paths = get_paths(matchers, options.top)
    delete_paths(paths)


if __name__ == "__main__":
    main()
