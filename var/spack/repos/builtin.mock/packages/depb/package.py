# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Depb(AutotoolsPackage):
    """Simple package with one build dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("pkg-b")

    def install(self, spec, prefix):
        # sanity_check_prefix requires something in the install directory
        # Test requires overriding the one provided by `AutotoolsPackage`
        mkdirp(prefix.bin)
