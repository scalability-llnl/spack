# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openturbine(CMakePackage, CudaPackage):
    """An open-source wind turbine structural dynamics simulation code."""

    license("MIT License", checked_by="ddement")

    homepage = "https://www.exascaleproject.org/research-project/exawind/"
    url = "https://github.com/Exawind/openturbine.git"
    git = "https://github.com/Exawind/openturbine.git"

    maintainers("faisal-bhuiyan", "ddement", "deslaughter")

    version("main", branch="main")

    variant("cuda", default=False, description="Compile using CUDA")
    variant("tests", default=False, description="Build OpenTurbine Test Suite")
    variant("coverage", default=False, description="Enable coverage reporting")
    variant("ipo", default=False, description="Enable Interprocedural Optimization")
    variant("werror", default=False, description="Treat warnings as errors")
    variant("address_sanitizer", default=False, description="Enable address sanitizer")
    variant("leak_sanitizer", default=False, description="Enable leak sanitizer")
    variant("ub_sanitizer", default=False, description="Enable undefined behavior sanitizer")
    variant("thread_sanitizer", default=False, description="Enable thread sanitizer")
    variant("memory_sanitizer", default=False, description="Enable memory sanitizer")
    variant("clang-tidy", default=False, description="Enable clang-tidy analysiis")
    variant("cppcheck", default=False, description="Enable CppCheck analysis")
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
    depends_on("trilinos+cuda+basker", when="+cuda")
    depends_on("kokkos-kernels~cuda", when="~cuda")
    depends_on("trilinos~cuda", when="~cuda")

    depends_on("llvm", when="+clang-tidy")

    depends_on("cppcheck", when="+cppcheck")

    depends_on("vtk", when="+vtk")

    depends_on("fortran", type="build", when="+adi")

    depends_on("fortran", type="build", when="+rosco")

    def cmake_args(self):
        options = []
        if self.spec.satisfies("+tests"):
            options.append("-DOpenTurbine_ENABLE_TESTS=ON")
        else:
            options.append("-DOpenTurbine_ENABLE_TESTS=OFF")
        if self.spec.satisfies("+coverage"):
            options.append("-DOpenTurbine_ENABLE_COVERAGE=ON")
        else:
            options.append("-DOpenTurbine_ENABLE_COVERAGE=OFF")
        if self.spec.satisfies("+ipo"):
            options.append("-DOpenTurbine_ENABLE_IPO=ON")
        else:
            options.append("-DOpenTurbine_ENABLE_IPO=OFF")
        if self.spec.satisfies("+werror"):
            options.append("-DOpenTurbine_WARNINGS_AS_ERRORS=ON")
        else:
            options.append("-DOpenTurbine_WARNINGS_AS_ERRORS=OFF")
        if self.spec.satisfies("+address_sanitizer"):
            options.append("-DOpenTurbine_ENABLE_SANITIZER_ADDRESS=ON")
        else:
            options.append("-DOpenTurbine_ENABLE_SANITIZER_ADDRESS=OFF")
        if self.spec.satisfies("+leak_sanitizer"):
            options.append("-DOpenTurbine_ENABLE_SANITIZER_LEAK=ON")
        else:
            options.append("-DOpenTurbine_ENABLE_SANITIZER_LEAK=OFF")
        if self.spec.satisfies("+ub_sanitizer"):
            options.append("-DOpenTurbine_ENABLE_SANITIZER_UNDEFINED=ON")
        else:
            options.append("-DOpenTurbine_ENABLE_SANITIZER_UNDEFINED=OFF")
        if self.spec.satisfies("+thread_sanitizer"):
            options.append("-DOpenTurbine_ENABLE_SANITIZER_THREAD=ON")
        else:
            options.append("-DOpenTurbine_ENABLE_SANITIZER_THREAD=OFF")
        if self.spec.satisfies("+memory_sanitizer"):
            options.append("-DOpenTurbine_ENABLE_SANITIZER_MEMORY=ON")
        else:
            options.append("-DOpenTurbine_ENABLE_SANITIZER_MEMORY=OFF")
        if self.spec.satisfies("+clang-tidy"):
            options.append("-DOpenTurbine_ENABLE_CLANG_TIDY=ON")
        else:
            options.append("-DOpenTurbine_ENABLE_CLANG_TIDY=OFF")
        if self.spec.satisfies("+cppcheck"):
            options.append("-DOpenTurbine_ENABLE_CPPCHECK=ON")
        else:
            options.append("-DOpenTurbine_ENABLE_CPPCHECK=OFF")
        if self.spec.satisfies("+vtk"):
            options.append("-DOpenTurbine_ENABLE_VTK=ON")
        else:
            options.append("-DOpenTurbine_ENABLE_VTK=OFF")
        if self.spec.satisfies("+adi"):
            options.append("-DOpenTurbine_BUILD_OPENFAST_ADI=ON")
        else:
            options.append("-DOpenTurbine_BUILD_OPENFAST_ADI=OFF")
        if self.spec.satisfies("+rosco"):
            options.append("-DOpenTurbine_BUILD_ROSCO_CONTROLLER=ON")
        else:
            options.append("-DOpenTurbine_BUILD_ROSCO_CONTROLLER=OFF")
        return options
