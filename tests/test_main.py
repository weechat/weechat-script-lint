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

"""Tests on main/init functions."""

from pathlib import Path

import sys

import mock
import pytest

import weechat_script_lint

SCRIPTS_DIR = Path(__file__).resolve().parent / 'scripts'


def test_main_no_scripts():
    """Test main function without scripts."""

    # no argument
    args = ['weechat-script-lint']
    with pytest.raises(SystemExit) as exc:
        with mock.patch.object(sys, 'argv', args):
            weechat_script_lint.main()
    assert exc.type == SystemExit
    assert exc.value.code == 2

    # display help
    args = ['weechat-script-lint', '--help']
    with pytest.raises(SystemExit) as exc:
        with mock.patch.object(sys, 'argv', args):
            weechat_script_lint.main()
    assert exc.type == SystemExit
    assert exc.value.code == 0


def test_main_script():
    """Test main function with a single script."""

    # script not found
    filename = str(SCRIPTS_DIR / 'unknown.py')
    args = ['weechat-script-lint', filename]
    with pytest.raises(SystemExit) as exc:
        with mock.patch.object(sys, 'argv', args):
            weechat_script_lint.main()
    assert exc.type == SystemExit
    assert 'FATAL' in exc.value.code

    # check script OK
    filename = str(SCRIPTS_DIR / 'script_valid.py')
    args = ['weechat-script-lint', filename]
    with pytest.raises(SystemExit) as exc:
        with mock.patch.object(sys, 'argv', args):
            weechat_script_lint.main()
    assert exc.type == SystemExit
    assert exc.value.code == 0


def test_main_dir():
    """Test main function with a directory."""

    # check directory with scripts
    args = [
        'weechat-script-lint',
        '--verbose',
        '--recursive',
        str(SCRIPTS_DIR),
    ]
    with pytest.raises(SystemExit) as exc:
        with mock.patch.object(sys, 'argv', args):
            weechat_script_lint.main()
    assert exc.type == SystemExit
    assert exc.value.code == 8

    # check directory with scripts, treat warnings as errors
    args = [
        'weechat-script-lint',
        '--strict',
        '--verbose',
        '--recursive',
        str(SCRIPTS_DIR),
    ]
    with pytest.raises(SystemExit) as exc:
        with mock.patch.object(sys, 'argv', args):
            weechat_script_lint.main()
    assert exc.type == SystemExit
    assert exc.value.code == 10

    args = [
        'weechat-script-lint',
        '--ignore-files', 'script_valid.py,script_missing_email.py',
        '--verbose',
        '--recursive',
        str(SCRIPTS_DIR),
    ]
    with pytest.raises(SystemExit) as exc:
        with mock.patch.object(sys, 'argv', args):
            weechat_script_lint.main()
    assert exc.type == SystemExit
    assert exc.value.code == 7

    # check a file that isn't a WeeChat script
    filename = str(SCRIPTS_DIR / 'not_a_script.txt')
    args = ['weechat-script-lint', '--verbose', filename]
    with pytest.raises(SystemExit) as exc:
        with mock.patch.object(sys, 'argv', args):
            weechat_script_lint.main()
    assert exc.type == SystemExit
    assert exc.value.code == 0


def test_init():
    """Test init function."""
    filename = str(SCRIPTS_DIR / 'script_valid.py')
    args = ['weechat-script-lint', filename]
    with pytest.raises(SystemExit) as exc:
        with mock.patch.object(weechat_script_lint, 'main', return_value=0):
            with mock.patch.object(weechat_script_lint,
                                   '__name__', '__main__'):
                with mock.patch.object(sys, 'argv', args):
                    weechat_script_lint.init(force=True)
    assert exc.type == SystemExit
    assert exc.value.code == 0
