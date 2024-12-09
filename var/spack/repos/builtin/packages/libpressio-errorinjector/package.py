# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpressioErrorinjector(CMakePackage):
    """LibPressioErrorInjector injects errors into data for sensitivity studies"""

    homepage = "https://github.com/robertu94/libpressio-errorinjector"
    git = "https://github.com/robertu94/libpressio-errorinjector"

    maintainers("robertu94")

    version("0.9.0", commit="7042a11ca94f2027e60e5824c7c72c7e9a07f80f")
    version("0.8.0", commit="0bfac9a06b1ae34a872b8b599dd4ccb46aa2db4e")
    version("0.7.0", commit="0b5a5b15121be248a3e5af925f9ad88b3d43fef6")

    depends_on("cxx", type="build")  # generated

    depends_on("libpressio@0.99.4:", when="@0.9.0:")
    depends_on("libpressio@0.88.0:", when="@0.8.0")
    depends_on("libpressio@:0.87.0", when="@0.7.0")

    def cmake_args(self):
        args = ["-DBUILD_TESTING=OFF"]
        return args
