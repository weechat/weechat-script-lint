#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2021-2025 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of weechat-script-lint.
#
# Weechat-script-lint is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Weechat-script-lint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with weechat-script-lint.  If not, see <https://www.gnu.org/licenses/>.
#

"""Static analysis tool for WeeChat scripts."""

from typing import Dict, Generator, List, Tuple

import argparse
import pathlib
import sys

from weechat_script_lint.script import WeechatScript
from weechat_script_lint.utils import color

__version__ = "0.6.0"

__all__ = (
    "__version__",
    "get_scripts",
    "main",
    "init",
)

SUPPORTED_SUFFIXES: Tuple[str, ...] = (
    ".js",
    ".lua",
    ".php",
    ".pl",
    ".py",
    ".rb",
    ".scm",
    ".tcl",
)


def get_parser() -> argparse.ArgumentParser:
    """
    Return the command line parser.

    :return: argument parser
    """
    parser = argparse.ArgumentParser(
        description="Static analysis tool for WeeChat scripts"
    )
    parser.add_argument(
        "-c",
        "--no-colors",
        action="store_true",
        help="do not use colors in output",
    )
    parser.add_argument(
        "-i",
        "--ignore-files",
        help="comma-separated list of file names to ignore",
    )
    parser.add_argument(
        "-l",
        "--level",
        choices=["error", "warning", "info"],
        default="info",
        help=(
            "level of messages to display: "
            "error = errors only, "
            "warning = errors and warnings, "
            "info = all messages"
        ),
    )
    parser.add_argument(
        "-m",
        "--ignore-messages",
        help="comma-separated list of error codes to ignore",
    )
    parser.add_argument(
        "-n",
        "--name-only",
        action="store_true",
        help=(
            "display only name of script but not the list of messages, "
            "do not display report and return code"
        ),
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="do not display any message",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="recursively find scripts in sub-directories",
    )
    parser.add_argument(
        "-s",
        "--strict",
        action="store_true",
        help="count warnings as errors in the returned code",
    )
    parser.add_argument(
        "-S",
        "--score",
        action="store_true",
        help=(
            "display scores by script, grouped by score, "
            "do not display report and return code"
        ),
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="verbose output"
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "path",
        nargs="+",
        type=pathlib.Path,
        help="path to a directory or a WeeChat script",
    )
    return parser


def get_scripts(
    path: pathlib.Path, args: argparse.Namespace, ignored_files: List[str]
) -> Generator[pathlib.Path, None, None]:
    """
    Return the list of scripts in a path.

    :param path: path (directory or file)
    :param args: command-line arguments
    :return: list of scripts
    """
    if path.is_dir():
        for path2 in path.iterdir():
            yield from get_scripts(path2, args, ignored_files)
    elif not path.is_file():
        sys.exit(f"FATAL: not a directory/file: {path}")
    elif not path.name.startswith(".") and path.suffix in SUPPORTED_SUFFIXES:
        if path.name in ignored_files:
            if not args.quiet and args.verbose:
                print(f"{path}: file ignored")
        else:
            yield path


def print_report(
    num_scripts: int,
    num_scripts_with_issues: int,
    count: Dict[str, int],
    use_colors: bool = True,
) -> None:
    """
    Print final report.

    :param num_scripts: number of script analyzed
    :param num_scripts_with_issues: number of scripts with issues
    :param count: counters (errors/warnings/info)
    :param use_colors: True to use colors in output
    """
    if num_scripts == 0:
        print("No scripts analyzed")
    else:
        colorize = color if use_colors else lambda x, y: x
        if sum(count.values()) == 0:
            status = colorize("Perfect", "bold,green")
        elif count["error"] + count["warning"] == 0:
            status = colorize("Almost good", "bold,cyan")
        elif count["error"] == 0:
            status = colorize("Not so good", "bold,yellow")
        else:
            status = colorize("FAILED", "bold,red")
        print(
            f"{status}: {num_scripts} scripts analyzed, "
            f"{num_scripts_with_issues} with issues: "
            f'{count["error"]} errors, '
            f'{count["warning"]} warnings, '
            f'{count["info"]} info'
        )


def get_string_score(score: int, use_colors: bool = True) -> str:
    """
    Get string with score.

    :param score: script score (between 0 and 100)
    :param use_colors: True to use colors in output
    """
    colorize = color if use_colors else lambda x, y: x
    if score < 50:
        status_color = "bold,red"
    elif score < 80:
        status_color = "bold,yellow"
    elif score < 100:
        status_color = "bold,cyan"
    else:
        status_color = "bold,green"
    return colorize(f"{score} / 100", status_color)


def print_scripts_by_score(
    scores: Dict[pathlib.Path, int], use_colors: bool = True
) -> None:
    """
    Print list of scripts grouped by score.

    :param scores: scores
    :param use_colors: True to use colors in output
    """
    scripts_by_score: Dict[int, List[pathlib.Path]] = {}
    for path, score in scores.items():
        scripts_by_score.setdefault(score, []).append(path)
    for score in sorted(scripts_by_score, reverse=True):
        sorted_paths = sorted(scripts_by_score[score])
        count_scripts = len(sorted_paths)
        paths = "\n".join([f"  {path}" for path in sorted_paths])
        print(
            f"{count_scripts} scripts "
            f"with score {get_string_score(score, use_colors)}:\n"
            f"{paths}"
        )


def print_scores(
    scores: Dict[pathlib.Path, int], use_colors: bool = True
) -> None:
    """
    Print scores for all checked scripts.

    :param name: script name
    :param score: script score (between 0 and 100)
    :param use_colors: True to use colors in output
    """
    for path, score in scores.items():
        str_score = get_string_score(score, use_colors)
        print(f"{path}: score = {str_score}")


def check_scripts(args: argparse.Namespace) -> Tuple[int, int]:
    """
    Check scripts.

    :param args: command-line arguments
    :return: number of errors found
    """
    count = {
        "error": 0,
        "warning": 0,
        "info": 0,
    }
    num_scripts = 0
    num_scripts_with_issues = 0
    scores: Dict[pathlib.Path, int] = {}
    ignored_files = (args.ignore_files or "").split(",")
    for path in args.path:
        scripts = get_scripts(path, args, ignored_files)
        for path_script in scripts:
            # check script
            num_scripts += 1
            script = WeechatScript(
                path=path_script,
                ignore=args.ignore_messages or "",
                use_colors=not args.no_colors,
                msg_level=args.level,
            )
            script.check()
            report = script.get_report(args.name_only)
            scores[path_script] = script.score
            if report:
                num_scripts_with_issues += 1
                if report and not args.quiet and not args.score:
                    print(report)
            # add errors/warnings/info found
            for counter in script.count:
                count[counter] += script.count[counter]
    if not args.quiet and args.score:
        print_scripts_by_score(scores, use_colors=not args.no_colors)
    if not args.quiet and not args.name_only and not args.score:
        print_scores(scores, use_colors=not args.no_colors)
    if not args.quiet and not args.name_only and not args.score:
        print_report(
            num_scripts,
            num_scripts_with_issues,
            count,
            use_colors=not args.no_colors,
        )
    return (count["error"], count["warning"])


def main() -> None:
    """Main function."""
    args = get_parser().parse_args()
    errors, warnings = check_scripts(args)
    ret_code = min(255, errors + warnings if args.strict else errors)
    if not args.quiet and not args.name_only and not args.score:
        print(f"Exiting with code {ret_code}")
    sys.exit(ret_code)


def init(force: bool = False) -> None:
    """Init function."""
    if __name__ == "__main__" or force:
        main()


init()
