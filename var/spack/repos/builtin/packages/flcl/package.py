# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Flcl(CMakePackage):
    """API for Fortran to C++ and C++ to Fortran multi-dimensional array
    interoperability using Kokkos."""

    homepage = "https://github.com/kokkos/kokkos-fortran-interop"
    git = "https://github.com/kokkos/kokkos-fortran-interop.git"
    url = "https://github.com/kokkos/kokkos-fortran-interop/releases/download/0.5.0/flcl-0.5.0.tar.gz"

    maintainers("womeld", "agaspar")

    license("BSD-3-Clause")

    version("develop", branch="develop")
    version("0.99.0", sha256="edb8310154e5e5cf315dad63cd59f13b2537e0ba698869ce9757b04e38047464")
    version("0.5.0", sha256="bfd9b9092904eab1135d3bb4c458a50653b3325c176a722af56f158da0a16f19")
    version("0.4.0", sha256="0fe327906a991262866b126a7d58098eb48297148f117fd59a2dbcc14e76f394")
    version("0.3", sha256="fc18c8fa3ae33db61203b647ad9025d894612b0faaf7fe07426aaa8bbfa9e703")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("kokkos")
    depends_on("cmake@3.17:", type="build", when="@:0.4.0")
    depends_on("cmake@3.19:", type="build", when="@0.5.0:")

    conflicts(
        "^kokkos@3.3.00:", when="@:0.4.99", msg="Requires FLCL >= 0.5.0 to use Kokkos >= 3.3"
    )

    def cmake_args(self):
        args = [self.define("BUILD_TESTING", self.run_tests)]
        return args
