### BackupChecker 

BackupChecker is an automated backup checker. Read the documentation in docs/
or [read it online](https://backupchecker.readthedocs.org/en/latest/).

If you would like, you can [support the development of this project on Liberapay](https://liberapay.com/carlchenet/).
Alternatively you can donate cryptocurrencies:

- BTC: 1BcdXCcLKN9PRpp6qw23FYkYuVp59dKZix
- XMR: 4Cxwvw9V6yUehv832FWPTF7FSVuWjuBarFd17QP163uxMaFyoqwmDf1aiRtS5jWgCiRsi73yqedNJJ6V1La2joznUDzkmvBr6KKHT7Dvzj

### Quick Install

* Install Backup Checker from PyPI

        # pip install backupchecker

* Install Backup Checker from sources

        # tar zxvf backupchecker-1.8.tar.gz
        # cd backupchecker
        # python3.4 setup.py install
        # # or
        # python3.4 setup.py install --install-scripts=/usr/bin

### Use Backup Checker locally

* Generate the configuration files for a given archive:

        $ backupchecker -G /path/to/backup.tar.gz

* Verify the archive and its content:

        $ backupchecker -c /path/to/confs/

### Use Backup Checker with remote backups

* Generate the configuration files for a remote archive through FTP

        $ wget --quiet -O - ftp://user:pass@server/backup.tar.gz | ./backupchecker.py -G -

* Verify an archive on a remote server through SSH

        $ ssh -q server "cat /tmp/backup.tar.gz" | ./backupchecker.py -c . -

### Authors

Carl Chenet <chaica@backupchecker.com>

### License

This software comes under the terms of the GPLv3+. See the LICENSE file for the complete text of the license.
