# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpliceA(Package):
    """Simple package with one optional dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/splice-a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789efghij")

    variant("foo", default=False, description="nope")
    variant("bar", default=False, description="nope")
    variant("baz", default=False, description="nope")

    depends_on("splice-z")
    depends_on("splice-z+foo", when="+foo")

    provides("something")
    provides("somethingelse")

    def install(self, spec, prefix):
        with open(prefix.join("splice-a"), "w") as f:
            f.write("splice-a: {0}".format(prefix))
            f.write("splice-z: {0}".format(spec["splice-z"].prefix))
