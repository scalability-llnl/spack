# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems._checks as checks
import spack.build_systems.generic
from spack.package import *


class TestBuildCallbacks(Package):
    """This package illustrates build callback test failure."""

    homepage = "http://www.example.com/test-build-callbacks"
    url = "http://www.test-failure.test/test-build-callbacks-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")


class GenericBuilder(spack.build_systems.generic.GenericBuilder):
    phases = ["build", "install"]

    # Include undefined method (runtime failure)
    build_time_test_callbacks = ["undefined-build-test"]
    run_after("build")(checks.execute_build_time_tests)

    def build(self, pkg, spec, prefix):
        pass

    def install(self, pkg, spec, prefix):
        mkdirp(prefix.bin)
