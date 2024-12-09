# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Datatransferkit(CMakePackage):
    """DataTransferKit is an open-source software library of
    parallel solution transfer services for multiphysics simulations"""

    homepage = "https://datatransferkit.readthedoc.io"
    url = "https://github.com/ORNL-CEES/DataTransferKit/archive/3.1.1.tar.gz"
    git = "https://github.com/ORNL-CEES/DataTransferKit.git"

    tags = ["e4s"]

    maintainers("Rombur")

    license("BSD-3-Clause")

    version("master", branch="master", submodules=True)
    version("3.1.1", commit="bfb7673cc233c26a6a541cbf096f37f26df1e5fb", submodules=True)
    version("3.1.0", commit="60a4cbd0a55505e0450f1ac979e1eef8966dc03f", submodules=True)
    version("3.1-rc3", commit="691d5a1540f7cd42141a3b3d2a7c8370cbc3560a", submodules=True)
    version("3.1-rc2", commit="1abc1a43b33dffc7a16d7497b4185d09d865e36a", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "external-arborx",
        default=False,
        description="use an external ArborX library instead of the submodule",
    )
    variant("openmp", default=False, description="enable OpenMP backend")
    variant("serial", default=True, description="enable Serial backend (default)")
    variant("shared", default=True, description="enable the build of shared lib")

    depends_on("mpi")
    depends_on("arborx@1.0:", when="+external-arborx")
    depends_on("boost")
    depends_on("cmake", type="build")
    depends_on("trilinos+intrepid2+shards~dtk")
    depends_on("trilinos+openmp", when="+openmp")
    depends_on("trilinos+stratimikos+belos", when="@master")
    depends_on("trilinos@13:13.4.1", when="@3.1-rc2:3.1-rc3")
    depends_on("trilinos@14.2:", when="@3.1.0:")

    def cmake_args(self):
        spec = self.spec
        from_variant = self.define_from_variant

        options = [
            from_variant("BUILD_SHARED_LIBS", "shared"),
            "-DDataTransferKit_ENABLE_DataTransferKit=ON",
            from_variant("DataTransferKit_ENABLE_ArborX_TPL", "external-arborx"),
            "-DDataTransferKit_ENABLE_TESTS=OFF",
            "-DDataTransferKit_ENABLE_EXAMPLES=OFF",
            "-DCMAKE_CXX_EXTENSIONS=OFF",
            "-DCMAKE_CXX_STANDARD=14",
            "-DCMAKE_C_COMPILER=" + spec["mpi"].mpicc,
            "-DCMAKE_CXX_COMPILER=" + spec["mpi"].mpicxx,
            "-DCMAKE_Fortran_COMPILER=" + spec["mpi"].mpifc,
            "-DMPI_BASE_DIR=" + spec["mpi"].prefix,
        ]

        if spec.satisfies("+openmp"):
            options.append("-DDataTransferKit_ENABLE_OpenMP=ON")

        return options
