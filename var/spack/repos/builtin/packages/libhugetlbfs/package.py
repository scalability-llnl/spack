# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libhugetlbfs(MakefilePackage):
    """libhugetlbfs is a library which provides easy access
       to huge pages of memory."""

    homepage = "https://github.com/libhugetlbfs/libhugetlbfs"
    url      = "https://github.com/libhugetlbfs/libhugetlbfs/releases/download/2.22/libhugetlbfs-2.22.tar.gz"

    version('2.22', sha256='94dca9ea2c527cd77bf28904094fe4708865a85122d416bfccc8f4b73b9a6785')

    def install(self, spec, prefix):
        make('install', "PREFIX=%s" % prefix)
