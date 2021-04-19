# weechat-script-lint

[![PyPI](https://img.shields.io/pypi/v/weechat-script-lint.svg)](https://pypi.org/project/weechat-script-lint/)
[![Build Status](https://github.com/weechat/weechat-script-lint/workflows/CI/badge.svg)](https://github.com/weechat/weechat-script-lint/actions?query=workflow%3A%22CI%22)

Weechat-script-lint is a static analysis tool for WeeChat scripts.

The script just requires Python ≥ 3.7.

## Installation

```
$ pip install weechat-script-lint
```

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
