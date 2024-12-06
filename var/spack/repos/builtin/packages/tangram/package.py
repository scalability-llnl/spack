# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tangram(CMakePackage):
    """Tangram is an material interface reconstruction package used in
    multimaterial ALE codes and multi-material remapping
    (https://github.com/laristra/portage)
    """

    homepage = "https://portage.lanl.gov"
    git = "https://github.com/laristra/tangram.git"
    url = "https://github.com/laristra/tangram/releases/download/1.0.5/tangram-1.0.5.tar.gz"

    maintainers("raovgarimella")

    license("GPL-3.0-or-later")

    version("1.0.5", sha256="4fa61d5fecd67215237ab3df8fe64bc6c4d018b22313f2174923486026e93e53")
    version("1.0.1", sha256="8f2f8c01bb2d726b0f64e5a5bc3aa2bd8057ccaee7a29c68f1439d16e39aaa90")
    version("master", branch="master", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=False, description="Enable interface reconstruction with MPI")
    variant("thrust", default=False, description="Enable on-node parallelism with NVidia Thrust")
    variant(
        "kokkos", default=False, description="Enable on-node or device parallelism with Kokkos"
    )
    variant("openmp", default=False, description="Enable on-node parallelism using OpenMP")
    variant("cuda", default=False, description="Enable GPU parallelism using CUDA")

    # wrappers to enable external mesh/state libraries (only for testing)
    variant("jali", default=False, description="Build with Jali mesh infrastructure (for testing)")

    # Don't enable Kokkos and Thrust simultaneously
    conflicts("+jali~mpi")  # Jali needs MPI
    conflicts("+thrust +cuda")  # We don't have Thrust with CUDA working yet
    conflicts("+thrust +kokkos")  # Don't enable Kokkos, Thrust simultaneously

    # dependencies
    depends_on("cmake@3.13:", type="build")

    depends_on("mpi", when="+mpi")
    #   Wonton depends array
    wonton_depends = ["mpi", "jali", "openmp", "thrust", "kokkos", "cuda"]

    for _variant in wonton_depends:
        depends_on("wonton+" + _variant, when="+" + _variant)
        depends_on("wonton~" + _variant, when="~" + _variant)

    def cmake_args(self):
        options = []
        if "+mpi" in self.spec:
            options.append("-DTANGRAM_ENABLE_MPI=ON")
        else:
            options.append("-DTANGRAM_ENABLE_MPI=OFF")

        if "+jali" in self.spec:
            options.append("-DTANGRAM_ENABLE_Jali=ON")
        else:
            options.append("-DTANGRAM_ENABLE_Jali=OFF")

        if "+thrust" in self.spec:
            options.append("-DTANGRAM_ENABLE_THRUST=ON")
        else:
            options.append("-DTANGRAM_ENABLE_THRUST=OFF")

        if "+kokkos" in self.spec:
            options.append("-DTANGRAM_ENABLE_Kokkos=ON")
        else:
            options.append("-DTANGRAM_ENABLE_Kokkos=OFF")

        # Unit test variant
        if self.run_tests:
            options.append("-DENABLE_UNIT_TESTS=ON")
            options.append("-DENABLE_APP_TESTS=ON")
        else:
            options.append("-DENABLE_UNIT_TESTS=OFF")
            options.append("-DENABLE_APP_TESTS=OFF")

        return options

    def check(self):
        if self.run_tests:
            with working_dir(self.build_directory):
                ctest("-j 8")
