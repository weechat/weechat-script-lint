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

"""Tests on utility functions."""

from weechat_script_lint import color


def test_color():  # pylint: disable=too-many-statements
    """Test color function."""
    assert color('', '') == ''
    assert color('test', '') == 'test'
    assert color('test', 'red') == '\x1b[31mtest\x1b[0m'
    assert color('test', 'red,bold') == '\x1b[31m\x1b[1mtest\x1b[0m'
