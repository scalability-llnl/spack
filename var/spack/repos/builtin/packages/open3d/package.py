# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Open3d(CMakePackage, CudaPackage):
    """Open3D: A Modern Library for 3D Data Processing."""

    homepage = "https://www.open3d.org/"
    url = "https://github.com/isl-org/Open3D/archive/refs/tags/v0.13.0.tar.gz"
    git = "https://github.com/isl-org/Open3D.git"

    license("MIT")

    version(
        "0.13.0", tag="v0.13.0", commit="c3f9de224e13838a72da0e5565a7ba51038b0f11", submodules=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("python", default=False, description="Build the Python module")

    # http://www.open3d.org/docs/latest/compilation.html

    depends_on("cmake@3.19:", type="build")
    # https://github.com/isl-org/Open3D/issues/3762
    # https://github.com/isl-org/Open3D/issues/4570
    depends_on("llvm@7:+clang")
    depends_on("eigen")
    depends_on("flann")
    # https://github.com/isl-org/Open3D/issues/4360
    # https://github.com/isl-org/Open3D/pull/5303
    depends_on("fmt@:7")
    depends_on("glew")
    depends_on("glfw")
    # depends_on('imgui')
    depends_on("jpeg")
    # depends_on('liblzf')
    depends_on("libpng")
    depends_on("py-pybind11")
    depends_on("qhull")
    # depends_on('tinygltf')
    # depends_on('tinyobjloader')

    extends("python", when="+python", type=("build", "link", "run"))
    depends_on("python@3.6:", when="+python", type=("build", "link", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-setuptools@40.8:", when="+python", type="build")
    depends_on("py-wheel@0.36:", when="+python", type="build")
    depends_on("py-numpy@1.18:", when="+python", type=("build", "run"))
    depends_on("py-pytest", when="+python", type="test")
    depends_on("cuda@10.1:", when="+cuda")

    # C++14 compiler required
    conflicts("%gcc@:4")
    conflicts("%clang@:6")

    # LLVM must be built with the C++ library
    conflicts("^llvm libcxx=none")

    def patch(self):
        # Force Python libraries to be installed to self.prefix
        filter_file(
            "pip install",
            "pip install --prefix " + self.prefix,
            os.path.join("cpp", "pybind", "make_install_pip_package.cmake"),
        )

    def cmake_args(self):
        return [
            self.define("BUILD_UNIT_TESTS", self.run_tests),
            self.define_from_variant("BUILD_PYTHON_MODULE", "python"),
            self.define_from_variant("BUILD_CUDA_MODULE", "cuda"),
            # https://github.com/isl-org/Open3D/issues/4570
            # self.define('BUILD_FILAMENT_FROM_SOURCE', 'ON'),
            # Use Spack-installed dependencies instead of vendored dependencies
            # Numerous issues with using externally installed dependencies:
            # https://github.com/isl-org/Open3D/issues/4333
            # https://github.com/isl-org/Open3D/issues/4360
            self.define("USE_SYSTEM_EIGEN3", True),
            self.define("USE_SYSTEM_FLANN", True),
            self.define("USE_SYSTEM_FMT", True),
            self.define("USE_SYSTEM_GLEW", True),
            self.define("USE_SYSTEM_GLFW", True),
            # self.define('USE_SYSTEM_IMGUI', True),
            self.define("USE_SYSTEM_JPEG", True),
            # self.define('USE_SYSTEM_LIBLZF', True),
            self.define("USE_SYSTEM_PNG", True),
            self.define("USE_SYSTEM_PYBIND11", True),
            self.define("USE_SYSTEM_QHULL", True),
            # self.define('USE_SYSTEM_TINYGLTF', True),
            # self.define('USE_SYSTEM_TINYOBJLOADER', True),
        ]

    def check(self):
        with working_dir(self.build_directory):
            tests = Executable(os.path.join("bin", "tests"))
            tests()

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make("install")
            if "+python" in spec:
                make("install-pip-package")

    # Tests don't pass unless all optional features are compiled, including PyTorch
    # @run_after('install')
    # @on_package_attributes(run_tests=True)
    # def unit_test(self):
    #     if '+python' in self.spec:
    #         pytest = which('pytest')
    #         pytest(os.path.join('python', 'test'))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_open3d_import(self):
        """Checking import of open3d"""
        if "+python" not in self.spec:
            return

        with working_dir("spack-test"):
            python = which(python.path)
            python("-c", "import open3d")
