from __future__ import annotations

import os
import typing
import shutil
from argparse import ArgumentParser

from gitignore_parser import parse_gitignore

if typing.TYPE_CHECKING:
    from argparse import Namespace


def get_paths(ign_file_path: str, parent: str) -> list[str]:
    """Get paths that match the patters given in ignore file."""

    paths: list[str] = []

    matches = parse_gitignore(ign_file_path)

    for path, dirs, filenames in os.walk(parent):
        for dir_ in dirs:
            if matches(dir_):
                dir_path = os.path.join(path, dir_)
                paths.append(dir_path)
            else:
                for filename in filenames:
                    file_path = os.path.join(path, filename)
                    if matches(file_path):
                        paths.append(file_path)

    paths = list(set(paths))
    return paths


def delete_paths(paths: list[str]) -> None:
    """Deletes each path in given paths."""

    for path in paths:
        if not os.path.exists(path):  # it is already deleted
            continue
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def parse_opts() -> Namespace:
    """Parse command line options and return Namespace object."""

    o_parser = ArgumentParser(
        prog="rm-ign",
        description="Delete every file (and folder) whose name matches"
                        " patterns defined in git ignore file."
    )
    add_opt = o_parser.add_argument

    add_opt(
        "-f",
        "--file",
        metavar="IGNORE",
        default=".gitignore",
        type=str,
        help="Path to ignore patterns file relative to present working directory."
                "Default is .gitignore."
    )
    add_opt(
        "-t",
        "--top",
        metavar="PATH",
        default=".",
        type=str,
        help="Path from where the deletion should start, recursively."
    )

    return o_parser.parse_args()


def main() -> None:
    options = parse_opts()
    if not os.path.exists(options.file):
        print("No `.gitignore` found in current directory.")
        return
    paths = get_paths(options.file, options.top)
    delete_paths(paths)


if __name__ == "__main__":
    main()
