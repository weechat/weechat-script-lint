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

"""Utility functions."""

from typing import Dict

__all__ = (
    'color',
)

COLORS: Dict[str, str] = {
    'black': '30',
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'magenta': '35',
    'cyan': '36',
    'reset_color': '49',
    'bold': '1',
    'underline': '4',
    'blink': '5',
    'reset_props': '0',
}


def color(text: str, colors: str) -> str:
    """
    Return a colored string (with ANSI codes).

    :param text: the text
    :param colors: comma-separated list of colors/attributes
        (eg: "green" or "bold,red")
    :return: string with color codes (no color codes if USE_COLORS is False)
    """
    if not colors:
        return text
    attrs = []
    for color_name in colors.split(','):
        attrs.append('\033[%sm' % COLORS.get(color_name, ''))
    return '%s%s\033[%sm' % (''.join(attrs),
                             str(text),
                             COLORS['reset_props'])
