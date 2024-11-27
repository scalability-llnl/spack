# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NoRedistributeDependent(AutotoolsPackage):
    """Package with one dependency on a package that should not be
    redistributed"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/no-redistribute-dependent-1.0.tar.gz"

    version("1.0", "0123456789abcdef0123456789abcdef")

    depends_on("no-redistribute")

    def install(self, spec, prefix):
        # sanity_check_prefix requires something in the install directory
        # Test requires overriding the one provided by `AutotoolsPackage`
        mkdirp(prefix.bin)
