# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.pkg.builtin.mock.python as mp
from spack.build_systems._checks import BaseBuilder, execute_install_time_tests
from spack.package import *


class PyTestCallback(mp.Python):
    """A package for testing stand-alone test methods as a callback."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/test-callback-1.0.tar.gz"

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "PyTestCallback"

    build_system("testcallback")

    version("1.0", "00000000000000000000000000000110")
    version("2.0", "00000000000000000000000000000120")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

    def test_callback(self):
        print("PyTestCallback test")


@spack.builder.builder("testcallback")
class MyBuilder(BaseBuilder):
    phases = ("install",)

    #: Callback names for install-time test
    install_time_test_callbacks = ["test_callback"]

    def install(self, pkg, spec, prefix):
        pkg.install(spec, prefix)

    spack.builder.run_after("install")(execute_install_time_tests)

    def test_callback(self):
        self.pkg.test_callback()
