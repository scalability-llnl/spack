# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Bricks(CMakePackage):
    """Bricks is a data layout and code generation framework,
    enabling performance-portable stencil computations across
    a multitude of architectures."""

    # url for your package's homepage here.
    homepage = "https://bricks.run/"
    git = "https://github.com/CtopCsUtahEdu/bricklib.git"

    test_requires_compiler = True

    # List of GitHub accounts to notify when the package is updated.
    maintainers("ztuowen", "drhansj")

    license("MIT")

    version("r0.1", branch="r0.1")
    version("2023.08.25", commit="d81725055c117c4b63a1b3835c6b634768b5bea7")  # no official release

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("cuda", default=False, description="Build bricks with CUDA enabled")

    # Building a variant of cmake without openssl is to match how the
    # ECP E4S project builds cmake in their e4s-base-cuda Docker image
    depends_on("cmake", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("opencl-clhpp", when="+cuda")
    depends_on("cuda", when="+cuda")
    depends_on("mpi")

    patch("bricks-cmakelists-option-opencl.patch")

    def cmake_args(self):
        """CMake arguments for configure stage"""
        args = [self.define_from_variant("BRICK_USE_OPENCL", "cuda")]
        if self.spec.satisfies("+cuda"):
            args.append(f"-DOCL_ROOT:STRING={self.spec['opencl-clhpp'].prefix}")
        return args

    def flag_handler(self, name, flags):
        """Set build flags as needed"""
        if name in ["cflags", "cxxflags", "cppflags"]:
            # There are many vector instrinsics used in this package. If
            # the package is built on a native architecture, then it likely
            # will not run (illegal instruction fault) on a less feature-
            # rich architecture.
            # If you intend to use this package in an architecturally-
            # heterogeneous environment, then the package should be build
            # with "target=x86_64". This will ensure that all Intel
            # architectures can use the libraries and tests in this
            # project by forceing the AVX2 flag in gcc.
            if name == "cxxflags" and self.spec.target == "x86_64":
                flags.append("-mavx2")
            return (None, flags, None)
        return (flags, None, None)

    @run_after("install")
    def copy_test_sources(self):
        """Files to copy into test cache"""
        srcs = [
            join_path("examples", "external", "CMakeLists.txt"),
            join_path("examples", "external", "main.cpp"),
            join_path("examples", "external", "7pt.py"),
        ]
        cache_extra_test_sources(self, srcs)

    def test_bricklib_example(self):
        """build and run pre-built example"""
        source_dir = join_path(self.test_suite.current_test_cache_dir, "examples", "external")
        if not os.path.exists(source_dir):
            raise SkipTest("{0} is missing".format(source_dir))

        with working_dir(source_dir):
            cmake = which(self.spec["cmake"].prefix.bin.cmake)
            cmake(".")

            cmake("--build", ".")

            example = which("example")
            example()
