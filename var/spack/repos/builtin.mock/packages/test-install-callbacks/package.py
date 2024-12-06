# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems._checks as checks
import spack.build_systems.generic
from spack.package import *


class TestInstallCallbacks(Package):
    """This package illustrates install callback test failure."""

    homepage = "http://www.example.com/test-install-callbacks"
    url = "http://www.test-failure.test/test-install-callbacks-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")


class GenericBuilder(spack.build_systems.generic.GenericBuilder):
    # Include an undefined callback method
    install_time_test_callbacks = ["undefined-install-test"]
    run_after("install")(checks.execute_install_time_tests)

    def install(self, pkg, spec, prefix):
        mkdirp(prefix.bin)
