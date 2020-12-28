# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nspr(AutotoolsPackage):
    """Netscape Portable Runtime (NSPR) provides a platform-neutral API
    for system level and libc-like functions."""

    homepage = "https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSPR"
    url      = "http://ftp.mozilla.org/pub/nspr/releases/v4.13.1/src/nspr-4.13.1.tar.gz"

    version('4.13.1', sha256='5e4c1751339a76e7c772c0c04747488d7f8c98980b434dc846977e43117833ab')

    depends_on('perl', type='build')

    configure_directory = 'nspr'

    def configure_args(self):
        return [
            '--with-mozilla',
            '--enable-64bit'  # without this, fails when 32-bit glibc not found
        ]
