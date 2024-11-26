# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SzCpp(CMakePackage):
    """Refactorization of SZ in cpp"""

    homepage = "https://github.com/robertu94/meta_compressor/"
    git = "https://github.com/robertu94/meta_compressor/"

    maintainers("robertu94")

    version("2022-01-27", commit="9441b79abc89d4bcce53fe18edf0df53fd92d1d7")

    depends_on("cxx", type="build")  # generated

    variant("shared", description="build shared libs", default=True)

    depends_on("zstd")
    depends_on("pkgconfig")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("BUILD_TESTING", self.run_tests),
        ]
        return args
