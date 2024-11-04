# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpliceVt(Package):
    """Simple package with one optional dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/splice-t-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("somethingelse")
    depends_on("splice-z")

    def install(self, spec, prefix):
        with open(prefix.join("splice-vt"), "w") as f:
            f.write("splice-vt: {0}".format(prefix))
            f.write("splice-h: {0}".format(spec["somethingelse"].prefix))
            f.write("splice-z: {0}".format(spec["splice-z"].prefix))
