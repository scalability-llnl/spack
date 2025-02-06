# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpliceDependsOnT(Package):
    """Package that depends on splice-t"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/splice-depends-on-t-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("splice-t")

    def install(self, spec, prefix):
        with open(prefix.join("splice-depends-on-t"), "w", encoding="utf-8") as f:
            f.write("splice-depends-on-t: {0}".format(prefix))
            f.write("splice-t: {0}".format(spec["splice-t"].prefix))
