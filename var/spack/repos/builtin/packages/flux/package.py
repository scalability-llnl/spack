# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Flux(CMakePackage):
    """A C++20 library for sequence-orientated programming"""

    homepage = "https://tristanbrindle.com/flux/"
    url = "https://github.com/tcbrindle/flux/archive/refs/tags/v0.4.0.tar.gz"

    maintainers("pranav-sivaraman")

    license("BSL-1.0", checked_by="pranav-sivaraman")

    version("0.4.0", sha256="95e7d9d71c9ee9e89bb24b46ccba77ddfb0a1580630c2faab0b415dacc7c8d56")

    variant("docs", default=False, description="Build Flux documentation")

    depends_on("cxx", type="build")
    depends_on("cmake@3.23:", type="build")

    with default_args(when="+docs"):
        depends_on("py-sphinx")
        depends_on("py-sphinx-copybutton")
        depends_on("py-furo")

    def cmake_args(self):
        args = [
            self.define("FLUX_BUILD_TESTS", self.run_tests),
            self.define("FLUX_BUILD_EXAMPLES", False),
            self.define_from_variant("FLUX_BUILD_DOCS", "docs"),
        ]

        return args
