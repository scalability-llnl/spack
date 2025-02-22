# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


def check(condition, msg):
    """Raise an install error if condition is False."""
    if not condition:
        raise InstallError(msg)


class MesonClient(MesonPackage):
    """A dummy package that uses meson."""

    homepage = "https://www.example.com"
    url = "https://www.example.com/meson-client-1.0.tar.gz"

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

    @run_after("meson")
    @run_before("meson")
    @run_before("build")
    @run_before("install")
    def increment(self):
        MesonClient.callback_counter += 1

    @run_after("meson")
    @on_package_attributes(run_this=True, check_this_is_none=None)
    def flip(self):
        MesonClient.flipped = True

    @run_after("meson")
    @on_package_attributes(does_not_exist=None)
    def do_not_execute(self):
        self.did_something = True

    def setup_build_environment(self, spack_env):
        spack_cc  # Ensure spack module-scope variable is available
        check(
            from_meson == "from_meson",
            "setup_build_environment couldn't read global set by meson.",
        )

        check(
            self.spec["meson"].link_arg == "test link arg",
            "link arg on dependency spec not readable from " "setup_build_environment.",
        )

    def setup_dependent_build_environment(self, env, dependent_spec):
        spack_cc  # Ensure spack module-scope variable is available
        check(
            from_meson == "from_meson",
            "setup_dependent_build_environment couldn't read global set by meson.",
        )

        check(
            self.spec["meson"].link_arg == "test link arg",
            "link arg on dependency spec not readable from " "setup_dependent_build_environment.",
        )

    def setup_dependent_package(self, module, dspec):
        spack_cc  # Ensure spack module-scope variable is available
        check(
            from_meson == "from_meson",
            "setup_dependent_package couldn't read global set by meson.",
        )

        check(
            self.spec["meson"].link_arg == "test link arg",
            "link arg on dependency spec not readable from " "setup_dependent_package.",
        )

    def meson(self, spec, prefix):
        assert self.callback_counter == 1

    def build(self, spec, prefix):
        assert self.did_something is False
        assert self.flipped is True
        assert self.callback_counter == 3

    def install(self, spec, prefix):
        assert self.callback_counter == 4
        # check that meson is in the global scope.
        global meson
        check(meson is not None, "No meson was in environment!")

        # check that which('meson') returns the right one.
        meson = which("meson")
        print(meson)
        print(meson.exe)
        check(
            meson.path.startswith(spec["meson"].prefix.bin),
            "Wrong meson was in environment: %s" % meson,
        )

        check(from_meson == "from_meson", "Couldn't read global set by meson.")

        check(
            os.environ["from_meson"] == "from_meson",
            "Couldn't read env var set in envieonmnt by dependency",
        )

        mkdirp(prefix.bin)
        touch(join_path(prefix.bin, "dummy"))
