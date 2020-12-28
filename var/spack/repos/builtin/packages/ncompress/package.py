# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ncompress(MakefilePackage):
    """This is (N)compress. It is an improved version of compress 4.1."""

    homepage = "https://vapier.github.io/ncompress/"
    url      = "https://github.com/vapier/ncompress/archive/v4.2.4.6.tar.gz"

    version('4.2.4.6',     sha256='112acfc76382e7b631d6cfc8e6ff9c8fd5b3677e5d49d3d9f1657bc15ad13d13')
    version('4.2.4.5',     sha256='2b532f02569e5557e1ed9cbe95c8db0e347a029517d3a50b906119808a996433')

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix))
