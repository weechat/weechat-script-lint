# SPDX-FileCopyrightText: 2021-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Tests on utility functions."""

from weechat_script_lint.utils import color, no_color


def test_color() -> None:
    """Test color function."""
    assert color("", "") == ""
    assert color("test", "") == "test"
    assert color("test", "red") == "\x1b[31mtest\x1b[0m"
    assert color("test", "red,bold") == "\x1b[31m\x1b[1mtest\x1b[0m"


def test_no_color() -> None:
    """Test color function."""
    assert no_color("") == ""
    assert no_color("", "") == ""
    assert no_color("test") == "test"
    assert no_color("test", "") == "test"
    assert no_color("test", "red") == "test"
