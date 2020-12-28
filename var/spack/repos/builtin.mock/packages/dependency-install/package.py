# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DependencyInstall(Package):
    """Dependency which has a working install method"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', 'hash1.0')
    version('2.0', 'hash2.0')

    def install(self, spec, prefix):
        touch(join_path(prefix, 'an_installation_file'))
