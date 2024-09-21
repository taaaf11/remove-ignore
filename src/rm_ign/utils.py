from __future__ import annotations

import typing
from argparse import ArgumentParser

from gitignore_parser import parse_gitignore

if typing.TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Callable, Sequence


def parse_opts() -> Namespace:
    """Parse command line options and return Namespace object."""

    o_parser = ArgumentParser(
        prog="rm-ign",
        description="Delete every file (and folder) whose name matches"
        " patterns defined in git ignore file.",
    )
    add_opt = o_parser.add_argument

    add_opt(
        "-f",
        "--files",
        metavar="FIlES",
        nargs="+",
        type=str,
        default=[".gitignore"],
        help="Path(s) to ignore patterns file(s). Defaults to $(pwd)/.gitignore.",
    )
    add_opt(
        "-t",
        "--top",
        metavar="PATH",
        default=".",
        type=str,
        help="Path from where the deletion should start, recursively."
        " Defaults to current directory.",
    )

    return o_parser.parse_args()


def make_matchers(full_paths: Sequence[str]) -> Sequence[Callable]:
    """Accepts a sequence of paths to git-ignore-patterns files,
    and returns a list of matcher functions based on patterns
    in the files.
    """

    return list(map(parse_gitignore, full_paths))


def match_matchers(path: str, matchers: Sequence[Callable]) -> bool:
    """Helper function to match a path against a sequence of
    matcher functions, returns True if path matches any of
    the matcher function.
    """

    for matcher in matchers:
        if matcher(path):
            return True
    return False
