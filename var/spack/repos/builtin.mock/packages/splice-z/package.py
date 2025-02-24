# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpliceZ(Package):
    """Simple package with one optional dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/splice-z-1.0.tar.gz"

    version("1.0.2")
    version("1.0.1")
    version("1.0.0")

    variant("foo", default=False, description="nope")
    variant("bar", default=False, description="nope")
    variant("compat", default=True, description="nope")

    can_splice("splice-z@1.0.0 +compat", when="@1.0.1 +compat")
    can_splice("splice-z@1.0.0:1.0.1 +compat", when="@1.0.2 +compat")

    def install(self, spec, prefix):
        with open(prefix.join("splice-z"), "w", encoding="utf-8") as f:
            f.write("splice-z: {0}".format(prefix))
