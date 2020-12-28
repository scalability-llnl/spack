# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Canfail(Package):
    """Package which fails install unless a special attribute is set"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    succeed = False

    def install(self, spec, prefix):
        if not self.succeed:
            raise InstallError("'succeed' was false")
        touch(join_path(prefix, 'an_installation_file'))
