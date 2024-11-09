# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Tiramisu(CMakePackage, CudaPackage, PythonExtension):
    """Tiramisu is a polyhedral compiler for dense and sparse deep learning
    and data parallel algorithms.It provides a simple C++ API for expressing
    algorithms and how these algorithms should be optimized by the compiler."""

    homepage = "http://tiramisu-compiler.org"
    url = "https://github.com/Tiramisu-Compiler/tiramisu"
    git = "https://github.com/Tiramisu-Compiler/tiramisu.git"

    maintainers("wraith1995")

    generator("ninja")

    license("MIT")

    version("master", branch="master")
    version("2023-2-8", commit="2cd0c43cc1656bfa43cfb6e81d06f770cbf7251e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("python", default=True, description="Install python bindings.")
    extends("python", when="+python")
    variant(
        "debug",
        default="0",
        description="Set the debug level.",
        multi=False,
        values=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"),
    )

    depends_on("cmake@3.5:", type="build")
    depends_on("halide@14.0.0:", type=("build", "link", "run"))
    depends_on("isl", type=("build", "link", "run"))
    depends_on("python@3.8:", type=("build", "link", "run"), when="+python")
    depends_on("py-pybind11@2.6.2:", type="build", when="+python")
    depends_on("py-numpy", type=("build", "run"), when="+python")
    depends_on("py-cython", type="run", when="+python")

    def cmake_args(self):
        spec = self.spec
        llvmdir = spec["llvm"].prefix.bin
        args = [
            self.define("HALIDE_LIB_DIRECTORY", spec["halide"].libs.directories[0]),
            self.define("LLVM_CONFIG_BIN", llvmdir),
            self.define("HALIDE_SOURCE_DIRECTORY", spec["halide"].prefix),
            self.define("ISL_INCLUDE_DIRECTORY", spec["isl"].headers.directories[0]),
            self.define("ISL_LIB_DIRECTORY", spec["isl"].libs.directories[0]),
            self.define_from_variant("DEBUG_LEVEL", "debug"),
            self.define_from_variant("WITH_PYTHON_BINDINGS", "python"),
            self.define_from_variant("USE_GPU", "cuda"),
            self.define("PYBIND11_USE_FETCHCONTENT", False),
            self.define("USE_FLEXNLP", False),
        ]
        if "+python" in spec:
            args += [self.define("Tiramisu_INSTALL_PYTHONDIR", python_platlib)]
        return args

    @property
    def build_targets(self):
        if "+python" in self.spec:
            return ["tiramisu", "Tiramisu_Python"]
        else:
            return ["tiramisu"]
