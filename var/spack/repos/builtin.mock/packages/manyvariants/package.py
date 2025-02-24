# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Manyvariants(Package):
    """
    A package with 4 different variants of different arities to test the
    `match_variants` argument to `can_splice`
    """

    homepage = "https://www.test.com"
    has_code = False

    version("2.0.1")
    version("2.0.0")
    version("1.0.1")
    version("1.0.0")

    variant("a", default=True)
    variant("b", default=False)
    variant("c", values=("v1", "v2", "v3"), multi=False, default="v1")
    variant("d", values=("v1", "v2", "v3"), multi=False, default="v1")

    can_splice("manyvariants@1.0.0", when="@1.0.1", match_variants="*")
    can_splice("manyvariants@2.0.0+a~b", when="@2.0.1~a+b", match_variants=["c", "d"])
    can_splice("manyvariants@2.0.0 c=v1 d=v1", when="@2.0.1+a+b")

    def install(self, spec, prefix):
        touch(prefix.bar)
