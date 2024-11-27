# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NetkitFtp(AutotoolsPackage):
    """netkit-ftp is the original file transfer client program for Linux."""

    homepage = "http://ftp.uk.linux.org/pub/linux/Networking/netkit"
    git = "https://github.com/mmaraya/netkit-ftp.git"

    license("BSD-4-Clause-UC")

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.man.man1)
        make("install")
