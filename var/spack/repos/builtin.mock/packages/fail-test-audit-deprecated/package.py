# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class FailTestAuditDeprecated(MakefilePackage):
    """Simple package attempting to implement and use deprecated stand-alone test methods."""

    homepage = "http://github.com/dummy/fail-test-audit-deprecated"
    url = "https://github.com/dummy/fail-test-audit-deprecated/archive/v1.0.tar.gz"

    version("2.0", sha256="c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1")
    version("1.0", sha256="abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234")

    @run_after("install")
    def copy_test_files(self):
        """test that uses the deprecated install_test_root method"""
        self.cache_extra_test_sources(".")

    def test(self):
        """this is a deprecated reserved method for stand-alone testing"""
        pass

    def test_use_install_test_root(self):
        """use the deprecated install_test_root method"""
        print(f"install test root = {self.install_test_root()}")

    def test_run_test(self):
        """use the deprecated run_test method"""
        self.run_test("which", ["make"])
