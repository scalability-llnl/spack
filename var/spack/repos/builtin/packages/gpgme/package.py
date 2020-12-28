# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gpgme(AutotoolsPackage):
    """GPGME is the standard library to access GnuPG
       functions from programming languages."""

    homepage = "https://www.gnupg.org/software/gpgme/index.html"
    url      = "https://www.gnupg.org/ftp/gcrypt/gpgme/gpgme-1.12.0.tar.bz2"

    executables = ['^gpgme-config$']

    version('1.12.0', sha256='b4dc951c3743a60e2e120a77892e9e864fb936b2e58e7c77e8581f4d050e8cd8')

    depends_on('gnupg', type='build')
    depends_on('libgpg-error', type='build')
    depends_on('libassuan', type='build')

    @classmethod
    def determine_version(cls, exe):
        return Executable(exe)('--version', output=str, error=str).rstrip()
