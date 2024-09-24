from __future__ import annotations

import os
import typing
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from gitignore_parser import parse_gitignore

from .actions import CustomHelpAction, VerInfoAction
from .types_ import MatcherFunctionType, StrOrPathLike
from .constants import PROG_DESC, PROG_NAME

if typing.TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Sequence


def parse_opts() -> Namespace:
    """Parse command line options and return Namespace object."""

    o_parser = ArgumentParser(
        prog=PROG_NAME,
        description=PROG_DESC,
        add_help=False,
        formatter_class=RawDescriptionHelpFormatter,
    )
    add_opt = o_parser.add_argument

    add_opt(
        "-f",
        "--files",
        metavar="FILES",
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
    add_opt(
        "-v",
        "--version",
        action=VerInfoAction,
    )
    add_opt(
        "-h",
        "--help",
        action=CustomHelpAction,
    )

    return o_parser.parse_args()


def make_matchers(paths: Sequence[StrOrPathLike]) -> Sequence[MatcherFunctionType]:
    """Accepts a sequence of paths to git-ignore-patterns files,
    and returns a sequence of matcher functions based on patterns
    in the files.
    """

    return tuple(parse_gitignore(path) for path in paths if os.path.exists(path))


def match_matchers(path: str, matchers: Sequence[MatcherFunctionType]) -> bool:
    """Helper function to match a path against a sequence of
    matcher functions, returns True if path matches any of
    the matcher function.
    """

    for matcher in matchers:
        if matcher(path):
            return True
    return False
