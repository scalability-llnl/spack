# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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

    version("0.10.0", sha256="d44142b302ffc193ad2229f1d2cc6d8d720dd9da8c37989ada4f23018f86c964")

    depends_on("cxx", type="build")  # generated

    variant("concepts", default=False, description="Enforce C++20 concepts")

    depends_on("cmake@3.18:", type="build")

    def cmake_args(self):
        args = [
            self.define("COVFIE_PLATFORM_CPU", True),
            self.define_from_variant("COVFIE_PLATFORM_CUDA", "cuda"),
            self.define_from_variant("COVFIE_REQUIRE_CXX20", "concepts"),
            self.define("COVFIE_QUIET", True),
        ]

        return args
