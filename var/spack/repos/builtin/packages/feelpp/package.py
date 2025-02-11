# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Feelpp(CMakePackage):
    """
    Feel++ is an Open-Source C++ library designed to solve a wide range of
    partial differential equations (PDEs) using advanced Galerkin methods.
    These methods include the finite element method (FEM), spectral element
    method, discontinuous Galerkin methods, and reduced basis methods.

    Feel++ is optimized for high-performance computing, enabling seamless
    parallel computing on large-scale systems, ranging from desktop machines
    to supercomputers with tens of thousands of cores. The library supports
    multi-physics simulations and provides a modular structure to simplify
    the development of applications.
    """

    homepage = "https://docs.feelpp.org"
    url = "https://github.com/feelpp/feelpp/archive/v0.110.2.tar.gz"
    git = "https://github.com/feelpp/feelpp.git"

    license = "LGPL-3.0-or-later AND GPL-3.0-or-later"
    maintainers = ["prudhomm", "vincentchabannes"]

    version("develop", branch="develop")
    version("preset", branch="2284-add-spack-environment-to-the-main-ci")

    # Define variants
    variant("toolboxes", default=True, description="Enable the Feel++ toolboxes")
    variant("mor", default=True, description="Enable Model Order Reduction (MOR)")
    variant("python", default=True, description="Enable Python wrappers")
    variant("quickstart", default=True, description="Enable the quickstart examples")
    variant("tests", default=False, description="Enable the tests")

    # Add variants for C++ standards
    variant(
        "cxxstd", default="20", description="C++ standard", values=["17", "20", "23"], multi=False
    )

    # Specify dependencies with required versions
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
    depends_on("cmake@3.21:", type="build")
    depends_on("llvm@14.0.0:")
    depends_on("mpi")
    depends_on("boost@1.74: +filesystem+iostreams+mpi+multithreaded+shared")
    depends_on("petsc@3.20 +mumps+hwloc+ptscotch +suite-sparse+hdf5 +hypre+kokkos")
    depends_on("slepc")
    depends_on("cln@1.3.6")
    depends_on("fftw")
    depends_on("libunwind")
    depends_on("libzip")
    depends_on("bison")
    depends_on("flex")
    depends_on("pugixml")
    depends_on("gsl")
    depends_on("glpk")
    depends_on("gl2ps")
    depends_on("ruby")
    depends_on("gmsh +opencascade+mmg+fltk")
    depends_on("curl")

    # Python dependencies if +python variant is enabled
    depends_on("py-pytest", when="+python")
    depends_on("py-pandas", when="+python")
    depends_on("py-petsc4py", when="+python")
    depends_on("py-slepc4py", when="+python")
    depends_on("py-numpy", when="+python")
    depends_on("py-pybind11", when="+python")
    depends_on("py-sympy", when="+python")
    depends_on("py-plotly", when="+python")
    depends_on("py-scipy", when="+python")
    depends_on("py-tabulate", when="+python")
    depends_on("py-ipykernel", when="+python")
    depends_on("py-mpi4py", when="+python")
    depends_on("py-tqdm", when="+python")
    depends_on("python@3.7:", when="+python", type=("build", "run"))

    def get_preset_name(self):
        spec = self.spec
        cpp_version = spec.variants["cxxstd"].value
        preset_name = f"feelpp-clang-cpp{cpp_version}-default-release"
        return preset_name

    def cmake_args(self):
        """Define the CMake preset and CMake options based on variants."""
        args = [
            f"--preset={self.get_preset_name()}",
            "-DFEELPP_ENABLE_VTK=OFF",
            "-DFEELPP_ENABLE_OPENTURNS=OFF",
            "-DFEELPP_ENABLE_OMC=OFF",
            "-DFEELPP_ENABLE_ANN=OFF",
            "-DFEELPP_USE_EXTERNAL_CLN=ON",
            self.define_from_variant("FEELPP_ENABLE_QUICKSTART", "quickstart"),
            self.define_from_variant("FEELPP_ENABLE_TESTS", "tests"),
            self.define_from_variant("FEELPP_ENABLE_TOOLBOXES", "toolboxes"),
            self.define_from_variant("FEELPP_ENABLE_MOR", "mor"),
            self.define_from_variant("FEELPP_ENABLE_FEELPP_PYTHON", "python"),
        ]
        return args

    def build(self, spec, prefix):
        cmake = which("cmake")
        cmake("--build", "--preset", self.get_preset_name())

    def install(self, spec, prefix):
        cmake = which("cmake")
        cmake("--build", "--preset", self.get_preset_name(), "-t", "install")

    def test(self, spec, prefix):
        ctest = which("ctest")
        ctest("--preset", self.get_preset_name(), "-R", "qs_laplacian")
