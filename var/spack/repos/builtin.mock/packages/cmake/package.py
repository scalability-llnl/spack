# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


def check(condition, msg):
    """Raise an install error if condition is False."""
    if not condition:
        raise InstallError(msg)


class Cmake(Package):
    """A dummy package for the cmake build system."""

    homepage = "https://www.cmake.org"
    url = "https://cmake.org/files/v3.4/cmake-3.4.3.tar.gz"

    version(
        "3.23.1",
        md5="4cb3ff35b2472aae70f542116d616e63",
        url="https://cmake.org/files/v3.4/cmake-3.4.3.tar.gz",
    )
    version(
        "3.4.3",
        md5="4cb3ff35b2472aae70f542116d616e63",
        url="https://cmake.org/files/v3.4/cmake-3.4.3.tar.gz",
    )

    def setup_build_environment(self, env):
        spack_cc  # Ensure spack module-scope variable is avaiable
        env.set("for_install", "for_install")

    def setup_dependent_build_environment(self, env, dependent_spec):
        spack_cc  # Ensure spack module-scope variable is avaiable
        env.set("from_cmake", "from_cmake")

    def setup_dependent_package(self, module, dspec):
        spack_cc  # Ensure spack module-scope variable is avaiable

        module.cmake = Executable(self.spec.prefix.bin.cmake)
        module.ctest = Executable(self.spec.prefix.bin.ctest)
        self.spec.from_cmake = "from_cmake"
        module.from_cmake = "from_cmake"

        self.spec.link_arg = "test link arg"

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        check(
            os.environ["for_install"] == "for_install",
            "Couldn't read env var set in compile envieonmnt",
        )
        cmake_exe_ext = ".exe" if sys.platform == "win32" else ""
        cmake_exe = join_path(prefix.bin, "cmake{}".format(cmake_exe_ext))
        touch(cmake_exe)
        set_executable(cmake_exe)
