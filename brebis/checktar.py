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

# Check a tar archive
'''Check a tar archive'''

import sys
import tarfile

from brebis.expectedvalues import ExpectedValues
from brebis.checkarchive import CheckArchive
import brebis.checkhashes

class CheckTar(CheckArchive):
    '''Check a tar archive'''

    def _main(self, _cfgvalues):
        '''Main for CheckTar'''
        _data = []
        _data, __arcdata = ExpectedValues(_cfgvalues['files_list']).data
        #########################
        # Test the archive itself
        #########################
        self._archive_checks(__arcdata, _cfgvalues['path'])
        ###############################
        # Test the files in the archive
        ###############################
        if _data:
            try:
                self._tar = tarfile.open(_cfgvalues['path'], 'r')
                for _tarinfo in self._tar:
                    __type = self.__translate_type(_tarinfo.type)
                    __arcinfo = {'path':_tarinfo.name, 'size':_tarinfo.size, 
                                    'uid':_tarinfo.uid, 'gid':_tarinfo.gid,
                                    'mode':_tarinfo.mode, 'type': __type}
                    _data = self._check_path(__arcinfo, _data)
                self._missing_files = [_file['path'] for _file in _data]
            except tarfile.TarError as _msg:
                print(_msg)

    def __translate_type(self, __arctype):
        '''Translate the type of the file inside the tar by a generic
        name
        '''
        __types = {tarfile.REGTYPE: 'f',
            tarfile.CHRTYPE: 'c',
            tarfile.DIRTYPE: 'd',
            tarfile.SYMTYPE: 's',
            tarfile.BLKTYPE: 'b',
            tarfile.FIFOTYPE: 'o'}
        return __types[__arctype]

    def _extract_stored_file(self, __arcfilepath):
        '''Extract a file from the archive and return a file object'''
        __file = self._tar.extractfile(__arcfilepath)
        return __file