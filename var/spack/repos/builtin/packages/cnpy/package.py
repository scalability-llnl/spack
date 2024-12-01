# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Cnpy(CMakePackage):
    """cnpy: library to read/write .npy and .npz files in C/C++."""

    homepage = "https://github.com/rogersce/cnpy"
    git = "https://github.com/rogersce/cnpy.git"

    license("MIT")

    version("master", branch="master")

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api", type="link")

    def cmake_args(self):
        args = []
        if sys.platform == "darwin":
            args.extend(["-DCMAKE_MACOSX_RPATH=ON"])

        return args
