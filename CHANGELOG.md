<!--
SPDX-FileCopyrightText: 2021-2026 Sébastien Helleu <flashcode@flashtux.org>

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Changelog

## [0.6.0] - 2025-04-20

### Changed

- Improve regex to detect e-mails

### Removed

- Remove warnings on deprecated infos `irc_nick_color` and `irc_nick_color_name` (used again with WeeChat >= 4.1.0)

### Added

- Add warnings `hook_process_url` and `hook_process_hashtable_url`
- Add infos `missing_spdx_copyright` and `missing_spdx_license`

## [0.5.1] - 2022-11-11

### Changed

- Add error `mixed_tabs_spaces` in README

## [0.5.0] - 2022-11-11

### Added

- Add error `mixed_tabs_spaces` for Python scripts

### Changed

- Allow deprecated stuff to be used if new names are used as well

## [0.4.0] - 2021-08-18

### Added

- Compute a score for each script, add option `-S` / `--score`
- Display a specific message when no scripts are analyzed
- Add status "FAILED" in report, display "Not so good" in yellow when there are no errors, display "Almost good" in cyan

## [0.3.0] - 2021-06-05

### Added

- Display report and return code
- Add option `-n` / `--name-only`
- Add option `-q` / `--quiet`

## [0.2.0] - 2021-04-21

### Added

- Add warnings on signals `irc_out_xxx` and `irc_outtags_xxx`
- Add warning on modifier `irc_in_xxx`
- Add warnings on deprecated infos `irc_nick_color` and `irc_nick_color_name`
- Add warnings on deprecated functions `hook_completion_get_string` and `hook_completion_list_add`

### Changed

- Sort messages by severity (high first)
- Check also empty files

### Fixed

- Fix duplicate errors on `python2_bin`

## [0.1.0] - 2021-04-19

### Added

- First release

[0.6.0]: https://github.com/weechat/weechat-script-lint/compare/v0.5.1...v0.6.0
[0.5.1]: https://github.com/weechat/weechat-script-lint/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/weechat/weechat-script-lint/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/weechat/weechat-script-lint/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/weechat/weechat-script-lint/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/weechat/weechat-script-lint/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/weechat/weechat-script-lint/releases/tag/v0.1.0
