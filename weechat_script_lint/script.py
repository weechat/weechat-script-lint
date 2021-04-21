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

"""WeeChat script linter."""

from typing import Dict, List, Tuple

import inspect
import pathlib
import re

from weechat_script_lint.utils import color

__all__ = (
    'WeechatScript',
)

LEVEL_LABELS: Dict[str, str] = {
    'error': 'bold,red',
    'warning': 'bold,yellow',
    'info': 'bold,green',
}

MESSAGES: Dict[str, Dict[str, str]] = {
    'error': {
        'missing_email': 'the author e-mail is missing',
        'missing_infolist_free': 'missing call to infolist_free',
        'python2_bin': 'the info python2_bin must not be used any more',
    },
    'warning': {
        'sys_exit': 'sys.exit() causes WeeChat to exit itself',
        'deprecated_hook_completion_get_string': (
            'function hook_completion_get_string is deprecated '
            'since WeeChat 2.9 and must be replaced by completion_get_string'
        ),
        'deprecated_hook_completion_list_add': (
            'function hook_completion_list_add is deprecated '
            'since WeeChat 2.9 and must be replaced by completion_list_add'
        ),
        'deprecated_irc_nick_color': (
            'info irc_nick_color is deprecated since WeeChat 1.5 '
            'and must be replaced by nick_color'
        ),
        'deprecated_irc_nick_color_name': (
            'info irc_nick_color_name is deprecated since WeeChat 1.5 '
            'and must be replaced by nick_color_name'
        ),
        'modifier_irc_in': (
            'modifier irc_in_{message} should be replaced by '
            'irc_in2_{message} which sends only valid UTF-8 data'
        ),
        'signal_irc_out': (
            'signal irc_out_{message} should be replaced by '
            'irc_out1_{message} which sends only valid UTF-8 data'
        ),
        'signal_irc_outtags': (
            'signal irc_outtags_{message} should be replaced by '
            'irc_out1_{message} which sends only valid UTF-8 data'
        ),
    },
    'info': {
        'unneeded_shebang': 'shebang not needed',
        'url_weechat': 'URL {link} should be changed to https://weechat.org',
    },
}

# note: this is not a valid e-mail regex; it is very permissive to detect
# only scripts that have no e-mail, even in an obfuscated form
EMAIL_REGEX = re.compile(
    # valid email with extra chars allowed (like # and * for obfuscation)
    r'([*#a-z0-9_.+-]+ ?(@| *at *) ?[*#a-z0-9-]+'
    r'(\.| *dot *)[a-z0-9-.]+)|'
    # <some.email>
    r'(<[a-z0-9_.+-]+>)',
    flags=re.IGNORECASE,
)


class ScriptMessage:  # pylint: disable=too-few-public-methods
    """A script message (error/warning/info)."""

    def __init__(self, path: pathlib.Path, level: str, msg_name: str,
                 line: int, **kwargs):
        self.path: pathlib.Path = path
        self.level: str = level
        self.msg_name: str = msg_name
        self.line: int = line
        self.text: str = MESSAGES[level][msg_name].format(**kwargs)

    def as_str(self, use_colors: bool = True):
        """Return formatted message."""
        label = (color(self.level, LEVEL_LABELS[self.level])
                 if use_colors else self.level)
        return (f'{self.path}:{self.line}: {label} [{self.msg_name}]: '
                f'{self.text}')


class WeechatScript:  # pylint: disable=too-many-instance-attributes
    """A WeeChat script."""

    def __init__(self, path: pathlib.Path, ignore: str = '',
                 msg_level: str = 'info', use_colors: bool = True):
        self.path: pathlib.Path = path.resolve()
        self.ignored_msg = [code.strip() for code in ignore.split(',') if code]
        self.msg_level: int = list(LEVEL_LABELS.keys()).index(msg_level)
        self.use_colors: bool = use_colors
        self.messages: List[ScriptMessage] = []
        self.count: Dict[str, int] = {label: 0 for label in LEVEL_LABELS}
        self.script: str = self.path.read_text()

    def __str__(self) -> str:
        """Return string with warnings/errors found."""
        return '\n'.join([
            msg.as_str(use_colors=self.use_colors)
            for msg in self.messages
        ])

    def message(self, level: str, msg_name: str, line: int = 1, **kwargs):
        """
        Add a message in the list of messages.

        :param level: type of message: "error", "warning", "info"
        :param msg_name: short name of message to display
        :param line: line number
        """
        if msg_name in self.ignored_msg \
                or self.msg_level < list(LEVEL_LABELS.keys()).index(level):
            return
        self.messages.append(
            ScriptMessage(self.path, level, msg_name, line, **kwargs)
        )
        self.count[level] += 1

    def search_regex(self, regex: str, flags: int = 0,
                     max_lines: int = 1) -> List[Tuple[int, re.Match]]:
        """
        Search a regular expression in each line of the script.
        A same line can be returned multiple times, if the string appears
        more than one time in the line.

        :param regex: regular expression to search
        :param flags: flags for call to re.compile()
        :param max_lines: max number of lines in each string found
        :return: list of tuples: (line_number, match)
        """
        pattern = re.compile(regex, flags=flags)
        occur = []
        for match in pattern.finditer(self.script):
            match_lines = match.group().count('\n') + 1
            if match_lines <= max_lines:
                line = match.string[:match.start()].count('\n') + 1
                occur.append((line, match))
        return occur

    def search_func(self, function: str, argument: str = '', flags: int = 0,
                    max_lines: int = 2) -> List[Tuple[int, re.Match]]:
        """
        Search a call to a function with the given argument.

        :param function: function (regex)
        :param argument: argument (regex)
        :param flags: flags for call to re.compile()
        :param max_lines: max number of lines in each string found
        :return: list of tuples: (line_number, match)
        """
        regex = fr'{function}[\s,(]*{argument}'
        return self.search_regex(regex, flags=flags, max_lines=max_lines)

    # === errors ===

    def _check_email(self):
        """Check if an e-mail is present."""
        if not re.search(EMAIL_REGEX, self.script):
            self.message('error', 'missing_email')

    def _check_infolist(self):
        """Check if infolist_free is called."""
        # if infolist_get is called, infolist_free must be called
        list_infolist_get = self.search_regex('infolist_get')
        count_infolist_free = self.script.count('infolist_free')
        if list_infolist_get and not count_infolist_free:
            for line_no, _ in list_infolist_get:
                self.message('error', 'missing_infolist_free', line=line_no)

    def _check_python2_bin(self):
        """Check if the info "python2_bin" is used."""
        if self.path.suffix == '.py':
            python2_bin = self.search_func('info_get', '["\']python2_bin["\']')
            for line_no, _ in python2_bin:
                self.message('error', 'python2_bin', line=line_no)

    # === warnings ===

    def _check_exit(self):
        """Check if an exit from the script can exit WeeChat."""
        if self.path.suffix == '.py':
            # Python sys.exit() function must never be called; it is only
            # a warning because it can be allowed when the import of weechat
            # module fails, which means the script is not running in WeeChat
            sys_exits = self.search_regex(r'sys\.exit')
            for line_no, _ in sys_exits:
                self.message('warning', 'sys_exit', line=line_no)

    def _check_deprecated_functions(self):
        """Check if deprecated functions are used."""
        # hook_completion_get_string is deprecated since WeeChat 2.9
        func = self.search_regex(r'hook_completion_get_string')
        for line_no, _ in func:
            self.message('warning', 'deprecated_hook_completion_get_string',
                         line=line_no)
        # hook_completion_list_add is deprecated since WeeChat 2.9
        func = self.search_regex(r'hook_completion_list_add')
        for line_no, _ in func:
            self.message('warning', 'deprecated_hook_completion_list_add',
                         line=line_no)

    def _check_deprecated_info(self):
        """Check if deprecated info are used."""
        # irc_nick_color is deprecated since WeeChat 1.5
        func = self.search_func('info_get', '["\']irc_nick_color["\']')
        for line_no, _ in func:
            self.message('warning', 'deprecated_irc_nick_color',
                         line=line_no)
        # irc_nick_color_name is deprecated since WeeChat 1.5
        func = self.search_func('info_get', '["\']irc_nick_color_name["\']')
        for line_no, _ in func:
            self.message('warning', 'deprecated_irc_nick_color_name',
                         line=line_no)

    def _check_modifier_irc_in(self):
        """Check if modifier irc_in_xxx is used."""
        func = self.search_func('hook_modifier', '["\']irc_in_([^"\']+)["\']')
        for line_no, match in func:
            self.message('warning', 'modifier_irc_in', line=line_no,
                         message=match.group(1))

    def _check_signals_irc_out(self):
        """Check if signals irc_out_xxx or irc_outtags_xxx are used."""
        func = self.search_func('hook_signal',
                                '["\'][^"\']+,irc_out_([^"\']+)["\']')
        for line_no, match in func:
            self.message('warning', 'signal_irc_out', line=line_no,
                         message=match.group(1))
        func = self.search_func('hook_signal',
                                '["\'][^"\']+,irc_outtags_([^"\']+)["\']')
        for line_no, match in func:
            self.message('warning', 'signal_irc_outtags', line=line_no,
                         message=match.group(1))

    # === info ===

    def _check_shebang(self):
        """Check if a sheband is present."""
        if self.script.startswith('#!'):
            self.message('info', 'unneeded_shebang')

    def _check_weechat_site(self):
        """Check if there are occurrences of wrong links to WeeChat site."""
        # https required, www not needed
        links = self.search_regex(
            r'(?:http://[w.]+weechat|https?://www.weechat)(?:\.org|\.net)',
            flags=re.IGNORECASE,
        )
        for line_no, match in links:
            self.message('info', 'url_weechat', line=line_no,
                         link=match.group())

    # run all checks, display report

    def check(self):
        """Perform checks on the script."""
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        methods.sort(key=lambda m: m[1].__func__.__code__.co_firstlineno)
        for name, method in methods:
            if name.startswith('_check_'):
                method()

    def print_report(self):
        """Print report, if any."""
        if self.messages:
            print(str(self))
