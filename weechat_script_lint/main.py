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

from typing import Generator, Tuple

import argparse
import pathlib
import sys

from weechat_script_lint.script import WeechatScript


__version__ = '0.1.0'

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
    else:
        yield path


def check_scripts(args) -> int:
    """
    Check scripts.

    :param argparse.Namespace args: command-line arguments
    :return: number of errors found
    """
    errors = 0
    ignored_files = (args.ignore_files or '').split(',')
    for path in args.path:
        scripts = get_scripts(path, args.recursive)
        for path_script in scripts:
            # ignore any unknown language or this script
            script_valid = (
                path_script.suffix in SUPPORTED_SUFFIXES
                and path_script.resolve() != pathlib.Path(__file__).resolve()
            )
            if not script_valid:
                if args.verbose:
                    print(f'{path_script}: not a WeeChat script, ignored')
                continue
            # ignored file?
            if path_script.name in ignored_files:
                if args.verbose:
                    print(f'{path_script}: file ignored')
                continue
            # check script
            script = WeechatScript(
                path=path_script,
                ignore=args.ignore_messages or '',
                use_colors=not args.no_colors,
                msg_level=args.level,
            )
            script.check()
            script.print_report()
            # add errors found
            errors += script.count['error']
            if args.strict:
                errors += script.count['warning']
    return errors


def main():
    """Main function."""
    args = get_parser().parse_args()
    errors = check_scripts(args)
    sys.exit(min(255, errors))


def init(force: bool = False):
    """Init function."""
    if __name__ == '__main__' or force:
        main()


init()
