# -*- coding: utf-8 -*-
# Copyright © 2009 Carl Chenet <chaica@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Brebis main
"""Brebis main"""

import sys

from cliparse import CliParse
from configurations import Configurations
from checkbackups import CheckBackups
from brebislogger import BrebisLogger

class Main(object):
    """The main class for Brebis"""

    def __init__(self):
        print('sys.argv:{}'.format(sys.argv))
        self.__main()

    def __main(self):
        _options = CliParse().options
        print(_options)
        BrebisLogger(_options.logfile)
        _confs = Configurations(_options.confpath)
        CheckBackups(_confs.configs)

