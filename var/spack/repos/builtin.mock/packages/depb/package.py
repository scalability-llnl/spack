# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Depb(Package):
    """Simple package with one direct dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("pkg-b")

    def install(self, spec, prefix):
        # sanity_check_prefix requires something in the install directory
        # `Package` does not define an `install` method by default
        mkdirp(prefix.bin)
