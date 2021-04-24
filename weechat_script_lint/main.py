#!/usr/bin/env python3
#
# Copyright (C) 2021 Sébastien Helleu <flashcode@flashtux.org>
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

from typing import Dict, Generator, Tuple

import argparse
import pathlib
import sys

from weechat_script_lint.script import WeechatScript
from weechat_script_lint.utils import color

__version__ = '0.3.0-dev'

__all__ = (
    '__version__',
    'get_scripts',
    'main',
    'init',
)

SUPPORTED_SUFFIXES: Tuple[str, ...] = (
    '.js',
    '.lua',
    '.php',
    '.pl',
    '.py',
    '.rb',
    '.scm',
    '.tcl',
)


def get_parser() -> argparse.ArgumentParser:
    """
    Return the command line parser.

    :return: argument parser
    """
    parser = argparse.ArgumentParser(
        description='Static analysis tool for WeeChat scripts')
    parser.add_argument('-c', '--no-colors', action='store_true',
                        help='do not use colors in output')
    parser.add_argument('-i', '--ignore-files',
                        help='comma-separated list of file names to ignore')
    parser.add_argument('-l', '--level',
                        choices=['error', 'warning', 'info'],
                        default='info',
                        help=('level of messages to display: '
                              'error = errors only, '
                              'warning = errors and warnings, '
                              'info = all messages'))
    parser.add_argument('-m', '--ignore-messages',
                        help='comma-separated list of error codes to ignore')
    parser.add_argument('-n', '--name-only', action='store_true',
                        help=('display only name of script but not the list '
                              'of messages, do not display report and return '
                              'code'))
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='do not display any message')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='recursively find scripts in sub-directories')
    parser.add_argument('-s', '--strict', action='store_true',
                        help='count warnings as errors in the returned code')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='verbose output')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('path', nargs='+', type=pathlib.Path,
                        help='path to a directory or a WeeChat script')
    return parser


def get_scripts(path: pathlib.Path,
                recursive: bool) -> Generator[pathlib.Path, None, None]:
    """
    Return the list of scripts in a path.

    :param path: path
    :param recursive: recursively list scripts in sub-directories
    :return: list of scripts
    """
    if path.is_dir():
        for path2 in path.iterdir():
            # ignore hidden files/directories
            if path2.name.startswith('.'):
                continue
            if path2.is_file():
                if path2.suffix in SUPPORTED_SUFFIXES:
                    yield path2
            elif recursive and path2.is_dir():
                yield from get_scripts(path2, recursive)
    elif not path.is_file():
        sys.exit(f'FATAL: not a directory/file: {path}')
    elif path.suffix in SUPPORTED_SUFFIXES:
        yield path


def print_report(num_scripts: int, num_scripts_with_issues: int,
                 count: Dict[str, int], use_colors: bool = True):
    """
    Print final report.

    :param num_scripts: number of script analyzed
    :param num_scripts_with_issues: number of scripts with issues
    :param count: counters (errors/warnings/info)
    :param use_colors: True to use colors in output
    """
    colorize = color if use_colors else lambda x, y: x
    if sum(count.values()) == 0:
        status = colorize('Perfect', 'bold,green')
    elif count['error'] + count['warning'] == 0:
        status = colorize('Almost good', 'bold,yellow')
    else:
        status = colorize('Not so good', 'bold,red')
    print(f'{status}: {num_scripts} scripts analyzed, '
          f'{num_scripts_with_issues} with issues: '
          f'{count["error"]} errors, '
          f'{count["warning"]} warnings, '
          f'{count["info"]} info')


def check_scripts(args) -> int:
    """
    Check scripts.

    :param argparse.Namespace args: command-line arguments
    :return: number of errors found
    """
    count = {
        'error': 0,
        'warning': 0,
        'info': 0,
    }
    num_scripts = 0
    num_scripts_with_issues = 0
    ignored_files = (args.ignore_files or '').split(',')
    for path in args.path:
        scripts = get_scripts(path, args.recursive)
        for path_script in scripts:
            # ignored file?
            if path_script.name in ignored_files:
                if not args.quiet and args.verbose:
                    print(f'{path_script}: file ignored')
                continue
            # check script
            num_scripts += 1
            script = WeechatScript(
                path=path_script,
                ignore=args.ignore_messages or '',
                use_colors=not args.no_colors,
                msg_level=args.level,
            )
            script.check()
            report = script.get_report(args.name_only)
            if report:
                num_scripts_with_issues += 1
                if report and not args.quiet:
                    print(report)
            # add errors/warnings/info found
            for counter in script.count:
                count[counter] += script.count[counter]
    if not args.quiet and not args.name_only:
        print_report(num_scripts, num_scripts_with_issues,
                     count, use_colors=not args.no_colors)
    if args.strict:
        return count['error'] + count['warning']
    return count['error']


def main():
    """Main function."""
    args = get_parser().parse_args()
    errors = check_scripts(args)
    ret_code = min(255, errors)
    if not args.quiet and not args.name_only:
        print(f'Exiting with code {ret_code}')
    sys.exit(ret_code)


def init(force: bool = False):
    """Init function."""
    if __name__ == '__main__' or force:
        main()


init()
