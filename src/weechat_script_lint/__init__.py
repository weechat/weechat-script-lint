# SPDX-FileCopyrightText: 2021-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Static analysis tool for WeeChat scripts."""

from weechat_script_lint.lint import lint


def main() -> None:
    """Run weechat-script-lint."""
    lint()
