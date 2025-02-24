# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hard(CMakePackage):
    """A FleCSI-based radiation-hydrodynamics solver suite
    for the study of astrophysical phenomena"""

    git = "https://github.com/lanl/hard"
    maintainers("JulienLoiseau")

    version("main", branch="main")

    variant("catalyst", default=False, description="Enable catalyst for paraview interface")
    variant("radiation", default=True, description="Enable support for radiation physics")
    variant("tests", default=False, description="Enable unit tests")

    depends_on("flecsi@2.3.0")
    depends_on("libcatalyst", when="+catalyst")
    depends_on("yaml-cpp@0.8:")

    def cmake_args(self):
        options = [
            self.define_from_variant("ENABLE_UNIT_TESTS", "tests"),
            self.define_from_variant("ENABLE_CATALYST", "catalyst"),
            self.define("DISABLE_RADIATION", self.spec.satisfies("~radiation")),
        ]

        return options
