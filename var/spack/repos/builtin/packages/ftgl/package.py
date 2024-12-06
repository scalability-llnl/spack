# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ftgl(CMakePackage):
    """Library to use arbitrary fonts in OpenGL applications."""

    homepage = "https://github.com/frankheckenbach/ftgl"
    git = "https://github.com/frankheckenbach/ftgl.git"

    license("MIT")

    version("master", branch="master")
    version("2.4.0", commit="483639219095ad080538e07ceb5996de901d4e74")
    version("2.3.1", commit="3c0fdf367824b6381f29df3d8b4590240db62ab7")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("shared", default=True, description="Build as a shared library")

    depends_on("cmake@2.8:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("gl")
    depends_on("glu")
    depends_on("freetype@2.0.9:")

    # Fix oversight in CMakeLists
    patch("remove-ftlibrary-from-sources.diff", when="@:2.4.0")

    # As reported by Khem Raj in
    # https://github.com/kraj/ftgl/commit/37ed7d606a0dfecdcb4ab0c26d1b0132cd96d5fa
    # freetype 2.13.3 changed the type of many external chars to unsigned char!
    patch(
        "https://patch-diff.githubusercontent.com/raw/frankheckenbach/ftgl/pull/20.patch?full_index=1",
        sha256="e2a0810fbf68403931bef4fbfda22e010e01421c92eeaa45f62e4e47f2381ebd",
        when="^freetype@2.13.3:",
    )

    def cmake_args(self):
        spec = self.spec
        args = ["-DBUILD_SHARED_LIBS={0}".format(spec.satisfies("+shared"))]

        # To not fail the build for 'char/unsigned char' conversion errors,
        # downgrade them to warnings in general to not fail the build:
        args.append("-DCMAKE_CXX_FLAGS=-fpermissive")

        if "darwin" in self.spec.architecture:
            args.append("-DCMAKE_MACOSX_RPATH=ON")
        return args

    # FIXME: See doc variant comment
    # @run_after('build')
    # def build_docs(self):
    #     if '+doc' in self.spec:
    #         cmake = self.spec['cmake'].command
    #         cmake('--build', '../spack-build', '--target', 'doc')
    #
    # @run_after('install')
    # def install_docs(self):
    #     if '+doc' in self.spec:
    #         cmake = self.spec['cmake'].command
    #         cmake('--install', '../spack-build', '--target', 'doc')
