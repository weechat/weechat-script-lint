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

"""Tests on WeechatScript class."""

from pathlib import Path

from weechat_script_lint import WeechatScript

SCRIPTS_DIR = Path(__file__).resolve().parent / 'scripts'

ALL_ERRORS = [
    ('error', 1, 'missing_email'),
    ('error', 17, 'missing_infolist_free'),
    ('error', 18, 'python2_bin'),
    ('warning', 27, 'sys_exit'),
    ('warning', 19, 'deprecated_hook_completion_get_string'),
    ('warning', 20, 'deprecated_hook_completion_list_add'),
    ('warning', 22, 'deprecated_irc_nick_color'),
    ('warning', 23, 'deprecated_irc_nick_color_name'),
    ('warning', 24, 'modifier_irc_in'),
    ('warning', 25, 'signal_irc_out'),
    ('warning', 26, 'signal_irc_outtags'),
    ('info', 1, 'unneeded_shebang'),
    ('info', 13, 'url_weechat'),
]


def test_script_valid():
    """Tests on a valid script."""
    path = SCRIPTS_DIR / 'script_valid.py'

    script = WeechatScript(path)
    assert str(script) == ''
    assert script.path == path.resolve()
    assert script.ignored_msg == []
    assert script.msg_level == 2
    assert script.use_colors is True
    assert script.messages == []
    assert script.count == {'error': 0, 'warning': 0, 'info': 0}
    assert script.script
    script.check()
    assert str(script) == ''
    assert script.count == {'error': 0, 'warning': 0, 'info': 0}


def test_script_all_errors():
    """Tests on a script with all possible messages."""
    path = SCRIPTS_DIR / 'script_all_errors.py'

    script = WeechatScript(path)
    assert str(script) == ''
    assert script.path == path.resolve()
    assert script.ignored_msg == []
    assert script.msg_level == 2
    assert script.use_colors is True
    assert script.messages == []
    assert script.count == {'error': 0, 'warning': 0, 'info': 0}
    assert script.script
    script.check()
    assert str(script)
    assert len(str(script).split('\n')) == 13
    assert script.count == {'error': 3, 'warning': 8, 'info': 2}
    errors = [
        (msg.level, msg.line, msg.msg_name)
        for msg in script.messages
    ]
    assert errors == ALL_ERRORS

    # ignore 2 messages: "missing_email" and "sys_exit"
    script = WeechatScript(path, ignore='missing_email,sys_exit')
    assert str(script) == ''
    assert script.path == path.resolve()
    assert script.ignored_msg == ['missing_email', 'sys_exit']
    assert script.msg_level == 2
    assert script.use_colors is True
    assert script.messages == []
    assert script.count == {'error': 0, 'warning': 0, 'info': 0}
    assert script.script
    script.check()
    assert str(script)
    assert len(str(script).split('\n')) == 11
    assert script.count == {'error': 2, 'warning': 7, 'info': 2}


def test_script_empty_file():
    """Tests on a script with all possible messages."""
    path = SCRIPTS_DIR / 'script_empty.py'
    script = WeechatScript(path)
    assert str(script) == ''
    assert script.path == path.resolve()
    assert script.ignored_msg == []
    assert script.msg_level == 2
    assert script.use_colors is True
    assert script.messages == []
    assert script.count == {'error': 0, 'warning': 0, 'info': 0}
    assert script.script == ''
    script.check()
    assert str(script)
    assert script.count == {'error': 1, 'warning': 0, 'info': 0}
