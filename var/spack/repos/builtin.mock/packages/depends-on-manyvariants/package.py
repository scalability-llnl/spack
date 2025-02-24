# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DependsOnManyvariants(Package):
    """
    A package with a dependency on `manyvariants`, so that `manyvariants` can
    be spliced in tests.
    """

    homepage = "https://www.test.com"
    has_code = False

    version("1.0")
    version("2.0")

    depends_on("manyvariants@1.0", when="@1.0")
    depends_on("manyvariants@2.0", when="@2.0")

    def install(self, spec, prefix):
        touch(prefix.bar)
