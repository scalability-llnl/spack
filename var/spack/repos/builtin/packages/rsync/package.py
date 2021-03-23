# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import re


class Rsync(AutotoolsPackage):
    """An open source utility that provides fast incremental file transfer."""
    homepage = "https://rsync.samba.org"
    url      = "https://download.samba.org/pub/rsync/src/rsync-3.1.2.tar.gz"

    version('3.2.2', sha256='644bd3841779507665211fd7db8359c8a10670c57e305b4aab61b4e40037afa8')
    version('3.1.3', sha256='55cc554efec5fdaad70de921cd5a5eeb6c29a95524c715f3bbf849235b0800c0')
    version('3.1.2', sha256='ecfa62a7fa3c4c18b9eccd8c16eaddee4bd308a76ea50b5c02a5840f09c0a1c2')
    version('3.1.1', sha256='7de4364fcf5fe42f3bdb514417f1c40d10bbca896abe7e7f2c581c6ea08a2621')

    depends_on('zlib')
    depends_on('popt')
    depends_on('openssl', when='@3.2:')
    depends_on('xxhash', when='@3.2:')
    depends_on('zstd', when='@3.2:')
    depends_on('lz4', when='@3.2:')

    conflicts('%nvhpc')

    executables = ['^rsync$']

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'rsync\s+version\s+(\S+)', output)
        return match.group(1) if match else None

    def configure_args(self):
        return ['--with-included-zlib=no']
