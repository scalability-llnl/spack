# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mdspan(CMakePackage):
    """Extension of std::span to enable multidimensional arrays"""

    homepage = "https://github.com/kokkos/mdspan/tree/stable"
    url = "https://github.com/kokkos/mdspan/archive/refs/tags/mdspan-0.6.0.zip"
    git = "https://github.com/kokkos/mdspan.git"

    version("stable", branch="stable")
    version("0.6.0", sha256="d6b7b9d4f472106df1d28729bd8383a8a7ea7938adf9f82d3be9c151344830d9")

    variant("examples", default=True, description="Enable examples")
    variant("tests", default=False, description="Enable tests")
    variant("benchmarks", default=False, description="Enable benchmarks")

    depends_on("benchmark", when="+benchmarks")
    depends_on("googletest@main", when="+tests")

    def cmake_args(self):
        args = []

        if self.spec.satisfies("+tests"):
            args.append("-DMDSPAN_ENABLE_TESTS=ON")
            args.append("-DMDSPAN_USE_SYSTEM_GTEST=ON")
        if self.spec.satisfies("+benchmarks"):
            args.append("-DMDSPAN_ENABLE_BENCHMARKS=ON")
        if self.spec.satisfies("+examples"):
            args.append("-DMDSPAN_ENABLE_EXAMPLES=ON")

        args.append("-DCMAKE_CXX_FLAGS='-Wall -Wextra -pedantic'")
        args.append("-DCMAKE_CXX_STANDARD=17")
        args.append("-DMDSPAN_CXX_STANDARD=17")
        args.append("-DCMAKE_CXX_COMPILER=g++")
        args.append("-DCMAKE_CXX_EXTENSIONS=OFF")

        return args
