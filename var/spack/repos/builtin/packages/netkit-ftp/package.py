# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NetkitFtp(AutotoolsPackage):
    """netkit-ftp is the original file transfer client program for Linux."""

    homepage = "http://ftp.uk.linux.org/pub/linux/Networking/netkit"
    git      = "https://github.com/mmaraya/netkit-ftp.git"

    version('master', branch='master')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.man.man1)
        make('install')
