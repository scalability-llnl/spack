# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class FailTestAudit(MakefilePackage):
    """Simple package attempting to re-use stand-alone test method as a build check."""

    homepage = "http://github.com/dummy/fail-test-audit"
    url = "https://github.com/dummy/fail-test-audit/archive/v1.0.tar.gz"

    version("2.0", sha256="c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1")
    version("1.0", sha256="abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234")

    # Stand-alone test methods cannot be included in build_time_test_callbacks
    build_time_test_callbacks = ["test_build_callbacks"]

    def test_build_callbacks(self):
        """test build time test callbacks failure"""
        print("test_build_callbacks")
