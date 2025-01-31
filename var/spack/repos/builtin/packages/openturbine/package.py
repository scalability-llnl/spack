# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openturbine(CMakePackage, CudaPackage, ROCmPackage):
    """An open-source wind turbine structural dynamics simulation code."""

    license("MIT License", checked_by="ddement")

    homepage = "https://www.exascaleproject.org/research-project/exawind/"
    url = "https://github.com/Exawind/openturbine.git"
    git = "https://github.com/Exawind/openturbine.git"

    maintainers("faisal-bhuiyan", "ddement", "deslaughter")

    version("main", branch="main")

    variant("tests", default=False, description="Build OpenTurbine Test Suite")
    variant("openmp", default=False, description="Build OpenTurbine with OpenMP support")
    variant("vtk", default=False, description="Enable VTK")
    variant("adi", default=False, description="Build the OpenFAST ADI external project")
    variant("rosco", default=False, description="Build the ROSCO controller external project")

    depends_on("cxx", type="build")
    depends_on("yaml-cpp")
    depends_on("kokkos-kernels+blas+lapack")
    depends_on("trilinos+amesos2")

    depends_on("kokkos-kernels@4.3:")
    depends_on("trilinos@16:")

    depends_on("kokkos-kernels+cuda+cublas+cusparse+cusolver", when="+cuda")
    depends_on("kokkos-kernels+rocblas+rocsparse+rocsolver", when="+rocm")
    depends_on("kokkos-kernels+openmp", when="+openmp")
    depends_on("trilinos+cuda+basker", when="+cuda")
    depends_on("trilinos+rocm+basker", when="+rocm")
    depends_on("trilinos+openmp+basker", when="+openmp")
    depends_on("kokkos-kernels~cuda", when="~cuda")
    depends_on("kokkos-kernels~openmp", when="~openmp")
    depends_on("trilinos~cuda", when="~cuda")
    depends_on("trilinos~rocm", when="~rocm")
    depends_on("trilinos~openmp", when="~openmp")

    depends_on("googletest", when="+tests")

    depends_on("vtk", when="+vtk")

    depends_on("fortran", type="build", when="+adi")

    depends_on("fortran", type="build", when="+rosco")

    def cmake_args(self):
        options = [
            self.define_from_variant("OpenTurbine_ENABLE_TESTS", "tests"),
            self.define_from_variant("OpenTurbine_ENABLE_VTK", "vtk"),
            self.define_from_variant("OpenTurbine_BUILD_OPENFAST_ADI", "adi"),
            self.define_from_variant("OpenTurbine_BUILD_ROSCO_CONTROLLER", "rosco"),
        ]
        return options
