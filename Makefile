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

all: check

check: lint test

lint: flake8 pylint mypy bandit

flake8:
	flake8 weechat_script_lint tests/*.py --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 weechat_script_lint tests/*.py --count --exit-zero --max-complexity=10 --statistics

pylint:
	pylint weechat_script_lint tests/*.py

mypy:
	mypy weechat_script_lint tests/*.py

bandit:
	bandit -r weechat_script_lint

test:
	pytest -vv --cov-report term-missing --cov=weechat_script_lint tests
