# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


def check(condition, msg):
    """Raise an install error if condition is False."""
    if not condition:
        raise InstallError(msg)


class CmakeClient(CMakePackage):
    """A dummy package that uses cmake."""

    homepage = "https://www.example.com"
    url = "https://www.example.com/cmake-client-1.0.tar.gz"

    version("1.0", md5="4cb3ff35b2472aae70f542116d616e63")

    variant(
        "multi",
        description="",
        values=any_combination_of("up", "right", "back").with_default("up"),
    )
    variant("single", description="", default="blue", values=("blue", "red", "green"), multi=False)
    variant("truthy", description="", default=True)

    callback_counter = 0

    flipped = False
    run_this = True
    check_this_is_none = None
    did_something = False

    @run_after("cmake")
    @run_before("cmake")
    @run_before("build")
    @run_before("install")
    def increment(self):
        CmakeClient.callback_counter += 1

    @run_after("cmake")
    @on_package_attributes(run_this=True, check_this_is_none=None)
    def flip(self):
        CmakeClient.flipped = True

    @run_after("cmake")
    @on_package_attributes(does_not_exist=None)
    def do_not_execute(self):
        self.did_something = True

    def setup_build_environment(self, spack_env):
        spack_cc  # Ensure spack module-scope variable is avaiabl
        check(
            from_cmake == "from_cmake",
            "setup_build_environment couldn't read global set by cmake.",
        )

        check(
            self.spec["cmake"].link_arg == "test link arg",
            "link arg on dependency spec not readable from " "setup_build_environment.",
        )

    def setup_dependent_build_environment(self, env, dependent_spec):
        spack_cc  # Ensure spack module-scope variable is avaiable
        check(
            from_cmake == "from_cmake",
            "setup_dependent_build_environment couldn't read global set by cmake.",
        )

        check(
            self.spec["cmake"].link_arg == "test link arg",
            "link arg on dependency spec not readable from " "setup_dependent_build_environment.",
        )

    def setup_dependent_package(self, module, dspec):
        spack_cc  # Ensure spack module-scope variable is avaiable
        check(
            from_cmake == "from_cmake",
            "setup_dependent_package couldn't read global set by cmake.",
        )

        check(
            self.spec["cmake"].link_arg == "test link arg",
            "link arg on dependency spec not readable from " "setup_dependent_package.",
        )

    def cmake(self, spec, prefix):
        assert self.callback_counter == 1

    def build(self, spec, prefix):
        assert self.did_something is False
        assert self.flipped is True
        assert self.callback_counter == 3

    def install(self, spec, prefix):
        assert self.callback_counter == 4
        # check that cmake is in the global scope.
        global cmake
        check(cmake is not None, "No cmake was in environment!")

        # check that which('cmake') returns the right one.
        cmake = which("cmake")
        print(cmake)
        print(cmake.exe)
        check(
            cmake.path.startswith(spec["cmake"].prefix.bin),
            "Wrong cmake was in environment: %s" % cmake,
        )

        check(from_cmake == "from_cmake", "Couldn't read global set by cmake.")

        check(
            os.environ["from_cmake"] == "from_cmake",
            "Couldn't read env var set in envieonmnt by dependency",
        )

        mkdirp(prefix.bin)
        touch(join_path(prefix.bin, "dummy"))
