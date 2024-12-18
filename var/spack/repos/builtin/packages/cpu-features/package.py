# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CpuFeatures(CMakePackage):
    """A cross platform C99 library to get cpu features at runtime."""

    homepage = "https://github.com/google/cpu_features"
    git = "https://github.com/google/cpu_features.git"
    url = "https://github.com/google/cpu_features/archive/refs/tags/v0.7.0.tar.gz"

    license("Apache-2.0")

    version("main", branch="main")
    version("develop", branch="main", deprecated=True)
    version("0.9.0", sha256="bdb3484de8297c49b59955c3b22dba834401bc2df984ef5cfc17acbe69c5018e")
    version("0.7.0", sha256="df80d9439abf741c7d2fdcdfd2d26528b136e6c52976be8bd0cd5e45a27262c0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", description="Build shared libraries", default=False)

    depends_on("cmake@3.0.0:", type="build")

    def cmake_args(self):
        args = ["-DBUILD_TESTING:BOOL=OFF"]
        args.append(self.define_from_variant("BUILD_SHARED_LIBS", variant="shared"))
        return args
