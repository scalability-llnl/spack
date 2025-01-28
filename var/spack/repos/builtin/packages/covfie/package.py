# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Covfie(CMakePackage, CudaPackage):
    """
    Covfie is a library for compositional descriptions of storage methods for
    vector fields and other structured multi-dimensional data.
    """

    homepage = "https://github.com/acts-project/covfie"
    url = "https://github.com/acts-project/covfie/archive/refs/tags/v0.1.0.tar.gz"
    list_url = "https://github.com/acts-project/covfie/tags"

    license("MPL-2.0")

    maintainers("stephenswat")

    version("0.11.0", sha256="39fcd0f218d3b4f3aacc6af497a8cda8767511efae7a72b47781f10fd4340f4f")
    version("0.10.0", sha256="d44142b302ffc193ad2229f1d2cc6d8d720dd9da8c37989ada4f23018f86c964")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.21:", type="build", when="@0.11:")
    depends_on("cmake@3.18:", type="build")

    def cmake_args(self):
        args = [
            self.define("COVFIE_PLATFORM_CPU", True),
            self.define_from_variant("COVFIE_PLATFORM_CUDA", "cuda"),
            self.define("COVFIE_QUIET", True),
        ]

        return args
