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

"""Tests on main/init functions."""

import sys
from pathlib import Path

import pytest

import weechat_script_lint
from weechat_script_lint.lint import get_status_color

SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"


def test_main_no_scripts(monkeypatch) -> None:
    """Test main function without scripts."""
    # no argument
    args = ["weechat-script-lint"]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc:
        weechat_script_lint.main()
    assert exc.value.code == 2

    # display help
    args = ["weechat-script-lint", "--help"]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc:
        weechat_script_lint.main()
    assert exc.value.code == 0


def test_main_script(monkeypatch) -> None:
    """Test main function with a single script."""
    # script not found
    filename = str(SCRIPTS_DIR / "unknown.py")
    args = ["weechat-script-lint", filename]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc:
        weechat_script_lint.main()
    assert "FATAL" in exc.value.code

    # check script OK
    filename = str(SCRIPTS_DIR / "script_valid.py")
    args = ["weechat-script-lint", filename]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc:
        weechat_script_lint.main()
    assert exc.value.code == 0


def test_main_dir(monkeypatch) -> None:
    """Test main function with a directory."""
    # check directory with scripts
    args = [
        "weechat-script-lint",
        "--verbose",
        "--recursive",
        str(SCRIPTS_DIR),
    ]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc:
        weechat_script_lint.main()
    assert exc.value.code == 10

    # check directory with scripts, treat warnings as errors
    args = [
        "weechat-script-lint",
        "--strict",
        "--verbose",
        "--recursive",
        str(SCRIPTS_DIR),
    ]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc:
        weechat_script_lint.main()
    assert exc.value.code == 26

    # check directory with scripts, display scripts by score
    args = [
        "weechat-script-lint",
        "--score",
        "--verbose",
        "--recursive",
        str(SCRIPTS_DIR),
    ]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc:
        weechat_script_lint.main()
    assert exc.value.code == 10

    args = [
        "weechat-script-lint",
        "--ignore-files",
        "script_valid.py,script_missing_email.py",
        "--verbose",
        "--recursive",
        str(SCRIPTS_DIR),
    ]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc:
        weechat_script_lint.main()
    assert exc.value.code == 9

    # check a script returning only a warning
    filename = str(SCRIPTS_DIR / "script_modifier_irc_in.py")
    args = [
        "weechat-script-lint",
        "--verbose",
        filename,
    ]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc:
        weechat_script_lint.main()
    assert exc.value.code == 0

    # check a script returning only an info
    filename = str(SCRIPTS_DIR / "script_unneeded_shebang.py")
    args = [
        "weechat-script-lint",
        "--verbose",
        filename,
    ]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc:
        weechat_script_lint.main()
    assert exc.value.code == 0

    # check a file that isn't a WeeChat script
    filename = str(SCRIPTS_DIR / "not_a_script.txt")
    args = ["weechat-script-lint", "--verbose", filename]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc:
        weechat_script_lint.main()
    assert exc.value.code == 0


def test_get_status_color() -> None:
    """Test function get_status_color."""
    assert get_status_color(-1) == ""
    assert get_status_color(101) == ""
    assert get_status_color(0) != ""
    assert get_status_color(100) != ""
    assert get_status_color(0) != get_status_color(80) != get_status_color(100)
