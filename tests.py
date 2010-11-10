#!/usr/bin/python3

import os
import logging
import sys
import unittest

import applogger
import checkbackups
import checkhashes
import checktar
import checktree
import checkzip
import cliparse
import configurations
from expectedfiles import ExpectedFiles
import main

# !! logging module uses a single logger for the whole file
TESTLOG = 'tests/testlog'

class TestApp(unittest.TestCase):

    def test_applogger(self):
        '''Test the AppLoggerclass'''
        applogger.AppLogger(TESTLOG)
        self.assertEqual(True, str(logging.getLogger('applogger')).startswith('<logging.Logger object at'))
        
    def test_checkbackup(self):
        '''Test the CheckBackup class'''
        _logfile = TESTLOG
        applogger.AppLogger(_logfile)
        checkbackups.CheckBackups({'essai': {'path': 'tests/tar_gz_archive_content/essai.tar.gz', 'files_list': 'tests/tar_gz_archive_content/essai-list', 'type': 'archive'}, 'essai2': {'path': 'tests/tar_bz2_archive_content/titi.tar.bz2', 'files_list': 'tests/tar_bz2_archive_content/essai2-list', 'type': 'archive'}})
        _res = open(_logfile).read()
        os.remove(_logfile)
        self.assertEqual(_res, 'WARNING:root:1 file missing in tests/tar_gz_archive_content/essai.tar.gz: \nWARNING:root:essai/dir/titi\n')

    def test_checkhashes_md5(self):
        '''Test the CheckHashes class with MD5'''
        _hashfile = 'tests/corrupted_archives/MD5SUMS'
        _hashtype = 'md5'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/md5-corrupted.tar.gz', 'type': 'archive'}}
        __checker = checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha1(self):
        '''Test the CheckHashes class with SHA1'''
        _hashfile = 'tests/corrupted_archives/SHA1SUMS'
        _hashtype = 'sha1'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha1-corrupted.tar.gz', 'type': 'archive'}}
        __checker = checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha224(self):
        '''Test the CheckHashes class with SHA224'''
        _hashfile = 'tests/corrupted_archives/SHA224SUMS'
        _hashtype = 'sha224'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha224-corrupted.tar.bz2', 'type': 'archive'}}
        __checker = checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha256(self):
        '''Test the CheckHashes class with SHA256'''
        _hashfile = 'tests/corrupted_archives/SHA256SUMS'
        _hashtype = 'sha256'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha256-corrupted.tar.gz', 'type': 'archive'}}
        __checker = checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha384(self):
        '''Test the CheckHashes class with SHA384'''
        _hashfile = 'tests/corrupted_archives/SHA384SUMS'
        _hashtype = 'sha384'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha384-corrupted.tar.bz2', 'type': 'archive'}}
        __checker = checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha512(self):
        '''Test the CheckHashes class with SHA512'''
        _hashfile = 'tests/corrupted_archives/SHA512SUMS'
        _hashtype = 'sha512'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha512-corrupted.tar.gz', 'type': 'archive'}}
        __checker = checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checktar_missing_files(self):
        '''Check if the CheckTar class returns a missing file'''
        _missingfiles = []
        _missingfiles = checktar.CheckTar({'path':
            'tests/tar_gz_archive_content/essai.tar.gz',
             'files_list':
                'tests/tar_gz_archive_content/essai-list',
             'type': 'archive'}).missing_files
        self.assertEqual(_missingfiles, ['essai/dir/titi'])

    def test_checktar_missing_equality(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality = []
        __missing_equality = checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'essai/dir/toto')

    def test_checktar_missing_bigger_than(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than = []
        __missing_bigger_than = checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'essai/titi')

    def test_checktar_missing_smaller_than(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than = []
        __missing_smaller_than = checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'essai/dir/toutou')

    def test_checktree_missing_files(self):
        '''Check if the CheckTar class returns a missing file'''
        __missing_files = []
        __missing_files = checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_files
        self.assertEqual(__missing_files, ['foo/bar/toto'])

    def test_checktree_missing_equality(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality= []
        __missing_equality = checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'foo/foo1')

    def test_checktree_missing_bigger_than(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than = []
        __missing_bigger_than = checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'foo/foo2')

    def test_checktree_missing_smaller_than(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than = []
        __missing_smaller_than = checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'foo/bar/foo3')

    def test_checkzip_missing_files(self):
        '''Check if the CheckZip class returns a missing file'''
        _missing_files = []
        _missing_files = checkzip.CheckZip({'path':
            'tests/zip_content/myzip.zip',
             'files_list':
                'tests/zip_content/myzip-list',
             'type': 'archive'}).missing_files
        self.assertEqual(_missing_files, ['toto/bling'])

    def test_checkzip_missing_equality(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality = []
        __missing_equality = checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'myzip/titi')

    def test_checkzip_missing_bigger_than(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than= []
        __missing_bigger_than = checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'myzip/foo/toto')

    def test_checkzip_missing_smaller_than(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than= []
        __missing_smaller_than = checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'myzip/toutou')

    def test_configurations(self):
        '''Test the Configurations class'''
        __path = 'tests/test_conf/'
        __res = configurations.Configurations(__path).configs
        self.assertEqual({'essai': {'path': 'tests/essai.tar.gz', 'files_list': 'tests/essai-list', 'type': 'archive', 'dbobjects': None, 'dbname': None, 'dbpath': None, 'dbhost': None, 'dbpass': None, 'dbuser': None, 'dbtype': None}}, __res)

    def test_expected_files(self):
        '''Check the ExpectedFiles class'''
        __data = ExpectedFiles('tests/file_size/essai-list').data
        self.assertEqual([{'path':'essai/dir/toto', 'equals':536870912},
            {'path':'essai/titi','biggerthan':536870912},
            {'path':'essai/dir/toutou','smallerthan':20480},
            {'path':'essai/dir/zozo'}], __data)

    def test_unexpected_files(self):
        '''Check if an unexpected file is identified'''
        __data = ExpectedFiles('tests/unexpected_files/files-list').data
        self.assertEqual([{'path':'foo/foo1'},{'path':'foo/foo2'},
            {'path':'foo/bar','unexpected':True}], __data)

if __name__ == '__main__':
    unittest.main()
