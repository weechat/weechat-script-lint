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


class WeechatScript:  # pylint: disable=too-many-instance-attributes
    """A WeeChat script."""

    def __init__(self, path: pathlib.Path, ignore: str = '',
                 msg_level: str = 'info', use_colors: bool = True):
        self.path: pathlib.Path = path.resolve()
        self.ignored_msg = [code.strip() for code in ignore.split(',') if code]
        self.msg_level: int = list(LEVEL_LABELS.keys()).index(msg_level)
        self.use_colors: bool = use_colors
        self.messages: List[str] = []
        self.count: Dict[str, int] = {label: 0 for label in LEVEL_LABELS}
        self.script: str = self.path.read_text()
        self.lines: List[str] = self.script.split('\n')

    def __str__(self) -> str:
        """Return string with warnings/errors found."""
        return '\n'.join(self.messages) if self.messages else ''

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
        label = (color(level, LEVEL_LABELS[level])
                 if self.use_colors else level)
        text = MESSAGES[level][msg_name].format(**kwargs)
        self.messages.append(f'{self.path}:{line}: {label} [{msg_name}]: '
                             f'{text}')
        self.count[level] += 1

    def search_regex(self,
                     regex: str,
                     flags: int = 0) -> List[Tuple[int, re.Match]]:
        """
        Search a regular expression in each line of the script.
        A same line can be returned multiple times, if the string appears
        more than one time in the line.

        :param regex: regular expression to search
        :param flags: flags for call to re.compile()
        :return: list of tuples: (line_number, match)
        """
        pattern = re.compile(regex, flags=flags)
        occur = []
        for i, line in enumerate(self.lines):
            matches = pattern.findall(line)
            for match in matches:
                occur.append((i + 1, match))
        return occur

    def check_shebang(self):
        """Check if a sheband is present."""
        if self.script.startswith('#!'):
            self.message('info', 'unneeded_shebang')

    def check_email(self):
        """Check if an e-mail is present."""
        if not re.search(EMAIL_REGEX, self.script):
            self.message('error', 'missing_email')

    def check_weechat_site(self):
        """Check if there are occurrences of wrong links to WeeChat site."""
        # http required, www not needed
        links = self.search_regex(
            r'(?:http://[w.]+weechat|https?://www.weechat)(?:\.org|\.net)',
            flags=re.IGNORECASE,
        )
        for line_no, link in links:
            self.message('info', 'url_weechat', line=line_no, link=link)

    def check_infolist(self):
        """Check if infolist_free is called."""
        list_infolist_get = self.search_regex('infolist_get')
        count_infolist_free = self.script.count('infolist_free')
        if list_infolist_get and not count_infolist_free:
            for line_no, _ in list_infolist_get:
                self.message('error', 'missing_infolist_free', line=line_no)

    def check_exit(self):
        """Check if an exit from the script can exit WeeChat."""
        if self.path.suffix == '.py':
            sys_exits = self.search_regex(r'sys\.exit')
            for line_no, _ in sys_exits:
                self.message('warning', 'sys_exit', line=line_no)

    def check_python2_bin(self):
        """Check if the info "python2_bin" is used."""
        if self.path.suffix == '.py':
            python2_bin = self.search_regex(r'python2_bin')
            for line_no, _ in python2_bin:
                self.message('error', 'python2_bin', line=line_no)

    def check(self):
        """Perform checks on the script."""
        if not self.script:
            return
        self.check_shebang()
        self.check_email()
        self.check_weechat_site()
        self.check_infolist()
        self.check_exit()
        self.check_python2_bin()

    def print_report(self):
        """Print report, if any."""
        if self.messages:
            print(str(self))
