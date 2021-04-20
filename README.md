# weechat-script-lint

[![PyPI](https://img.shields.io/pypi/v/weechat-script-lint.svg)](https://pypi.org/project/weechat-script-lint/)
[![Build Status](https://github.com/weechat/weechat-script-lint/workflows/CI/badge.svg)](https://github.com/weechat/weechat-script-lint/actions?query=workflow%3A%22CI%22)

Weechat-script-lint is a static analysis tool for WeeChat scripts.

It can be used by people writing WeeChat scripts and it is automatically
executed in the CI of the WeeChat official scripts repository:
[https://github.com/weechat/scripts/](https://github.com/weechat/scripts/).

## Installation

The script requires Python ≥ 3.7.

In a Python virtual environment:

```
$ pip install weechat-script-lint
```

## Checks

When a script is checked, problems are displayed on output, with one of these
levels:

- `error`: severe problem, the script must be fixed now (the return code of
  command is the number of errors)
- `warning`: a deprecated feature is used (script may break in future) or there
  is a minor problem, the script should be fixed
- `info`: information; no urgent fix needed.

### Error: missing_email

This is a problem if the script is submitted in the official scripts repository
where the e-mail is required.

In other cases, the error can be ignored.

### Error: missing_infolist_free

When an infolist is asked to WeeChat with `infolist_get`, it must always be
freed by a call to `infolist_free`, otherwise this causes a memory leak.

### Error: python2_bin

The info `python2_bin` is used to find the path to Python 2.x interpreter.
Since WeeChat is compiled with Python 3 and that all scripts aim to be
compatible with Python 3, this info must not be used at all any more.

Moreover, some systems don't include Python 2 any more.

### Warning: sys_exit (Python)

The function `sys.exit()` causes WeeChat to exit itself, so it must not be used
in scripts.

This is a warning and not an error because if it is used when the import of
`weechat` fails, that means the script is not executed in WeeChat and then the
call to `sys.exit()` is harmless.

### Warning: deprecated_hook_completion_get_string

The function `hook_completion_get_string` is deprecated and should not be used
any more since WeeChat 2.9.

The function `completion_get_string` must be used instead.

### Warning: deprecated_hook_completion_list_add

The function `hook_completion_list_add` is deprecated and should not be used
any more since WeeChat 2.9.

The function `completion_list_add` must be used instead.

### Warning: deprecated_irc_nick_color

The info `irc_nick_color` is deprecated and should not be used any more
since WeeChat 1.5.

The info `nick_color` must be used instead.

### Warning: deprecated_irc_nick_color_name

The info `irc_nick_color_name` is deprecated and should not be used any more
since WeeChat 1.5.

The info `nick_color_name` must be used instead.

### Info: unneeded_shebang

The shebang is not needed, except if the script can be called outside WeeChat,
which is rare.

### Info: url_weechat

The WeeChat site URL is https://weechat.org (`https` and no `www`).

## Example

```
$ weechat-script-lint script.py
/path/to/script.py:44: info [url_weechat]: URL http://www.weechat.org should be changed to https://weechat.org
/path/to/script.py:45: warning [sys_exit]: sys.exit() causes WeeChat to exit itself
/path/to/script.py:98: error [python2_bin]: the info python2_bin must not be used any more
/path/to/script.py:167: error [missing_infolist_free]: missing call to infolist_free
```

## Copyright

Copyright © 2021 [Sébastien Helleu](https://github.com/flashcode)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
