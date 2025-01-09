# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpliceH(Package):
    """Simple package with one optional dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/splice-h-1.0.tar.gz"

    version("1.0.2")
    version("1.0.1")
    version("1.0.0")

    variant("foo", default=False, description="nope")
    variant("bar", default=False, description="nope")
    variant("baz", default=False, description="nope")
    variant("compat", default=True, description="nope")

    depends_on("splice-z")
    depends_on("splice-z+foo", when="+foo")

    provides("something")
    provides("somethingelse")
    provides("virtual-abi")

    can_splice("splice-h@1.0.0 +compat", when="@1.0.1 +compat")
    can_splice("splice-h@1.0.0:1.0.1 +compat", when="@1.0.2 +compat")

    def install(self, spec, prefix):
        with open(prefix.join("splice-h"), "w", encoding="utf-8") as f:
            f.write("splice-h: {0}".format(prefix))
            f.write("splice-z: {0}".format(spec["splice-z"].prefix))
