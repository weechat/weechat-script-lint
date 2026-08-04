# SPDX-FileCopyrightText: 2021-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Utility functions."""

COLORS: dict[str, str] = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "reset_color": "49",
    "bold": "1",
    "underline": "4",
    "blink": "5",
    "reset_props": "0",
}


def color(text: str, colors: str) -> str:
    """Return a colored string (with ANSI codes).

    :param text: the text
    :param colors: comma-separated list of colors/attributes
        (eg: "green" or "bold,red")
    :return: string with color codes (no color codes if USE_COLORS is False)
    """
    if not colors:
        return text
    attrs = [f"\033[{COLORS.get(color_name, '')}m" for color_name in colors.split(",")]
    return f"{''.join(attrs)}{text}\033[{COLORS['reset_props']}m"


def no_color(text: str, *args: str) -> str:  # noqa: ARG001
    """Return text as-is."""
    return text
