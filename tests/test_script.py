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

"""Tests on WeechatScript class."""

from pathlib import Path

from weechat_script_lint import WeechatScript

SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"

ALL_ERRORS = [
    ("error", 1, "missing_email"),
    ("error", 17, "missing_infolist_free"),
    ("error", 18, "python2_bin"),
    ("error", 1, "mixed_tabs_spaces"),
    ("warning", 27, "sys_exit"),
    ("warning", 19, "deprecated_hook_completion_get_string"),
    ("warning", 20, "deprecated_hook_completion_list_add"),
    ("warning", 22, "modifier_irc_in"),
    ("warning", 23, "signal_irc_out"),
    ("warning", 24, "signal_irc_outtags"),
    ("warning", 25, "hook_process_url"),
    ("warning", 26, "hook_process_hashtable_url"),
    ("info", 1, "unneeded_shebang"),
    ("info", 13, "url_weechat"),
    ("info", 1, "missing_spdx_copyright"),
    ("info", 1, "missing_spdx_license"),
]


def test_script_valid() -> None:
    """Tests on a valid script."""
    path = SCRIPTS_DIR / "script_valid.py"

    script = WeechatScript(path)
    assert str(script) == ""
    assert script.path == path.resolve()
    assert script.ignored_msg == []
    assert script.msg_level == 2
    assert script.use_colors is True
    assert not script.messages
    assert script.count == {"error": 0, "warning": 0, "info": 0}
    assert script.script
    script.check()
    assert str(script) == ""
    assert script.count == {"error": 0, "warning": 0, "info": 0}
    assert script.get_report(False) == ""
    assert script.get_report(True) == ""


def test_script_all_errors() -> None:
    """Tests on a script with all possible messages."""
    path = SCRIPTS_DIR / "script_all_errors.py"

    script = WeechatScript(path)
    assert str(script) == ""
    assert script.path == path.resolve()
    assert script.ignored_msg == []
    assert script.msg_level == 2
    assert script.use_colors is True
    assert not script.messages
    assert script.count == {"error": 0, "warning": 0, "info": 0}
    assert script.script
    script.check()
    assert str(script)
    assert len(str(script).split("\n")) == len(ALL_ERRORS)
    print(script.count)
    assert script.count == {"error": 4, "warning": 8, "info": 4}
    errors = [(msg.level, msg.line, msg.msg_name) for msg in script.messages]
    assert errors == ALL_ERRORS
    assert len(script.get_report(False).split("\n")) == len(ALL_ERRORS)
    assert script.get_report(True) == "script_all_errors.py"

    # ignore 2 messages: "missing_email" and "sys_exit"
    script = WeechatScript(path, ignore="missing_email,sys_exit")
    assert str(script) == ""
    assert script.path == path.resolve()
    assert script.ignored_msg == ["missing_email", "sys_exit"]
    assert script.msg_level == 2
    assert script.use_colors is True
    assert not script.messages
    assert script.count == {"error": 0, "warning": 0, "info": 0}
    assert script.script
    script.check()
    assert str(script)
    assert len(str(script).split("\n")) == len(ALL_ERRORS) - 2
    assert script.count == {"error": 3, "warning": 7, "info": 4}
    assert len(script.get_report(False).split("\n")) == len(ALL_ERRORS) - 2
    assert script.get_report(True) == "script_all_errors.py"


def test_script_empty_file() -> None:
    """Tests on a script with all possible messages."""
    path = SCRIPTS_DIR / "script_empty.py"
    script = WeechatScript(path)
    assert str(script) == ""
    assert script.path == path.resolve()
    assert script.ignored_msg == []
    assert script.msg_level == 2
    assert script.use_colors is True
    assert not script.messages
    assert script.count == {"error": 0, "warning": 0, "info": 0}
    assert script.script == ""
    script.check()
    assert str(script)
    assert script.count == {"error": 1, "warning": 0, "info": 2}
    assert len(script.get_report(False).split("\n")) == 3
    assert script.get_report(True) == "script_empty.py"
