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

from codecs import open
from setuptools import setup, find_packages
from weechat_script_lint import __version__ as wsl_version

DESCRIPTION = "Static analysis tool for WeeChat scripts."

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

setup(
    name="weechat-script-lint",
    version=wsl_version,
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Sébastien Helleu",
    author_email="flashcode@flashtux.org",
    url="https://github.com/weechat/weechat-script-lint",
    license="GPL3",
    keywords="static analysis weechat script lint",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 "
        "or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    tests_require=["pytest"],
    entry_points={
        "console_scripts": ["weechat-script-lint=weechat_script_lint:main"],
    },
)
