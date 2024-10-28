# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class FailTestAuditImpl(MakefilePackage):
    """Simple package that is missing the stand-alone test implementation."""

    homepage = "http://github.com/dummy/fail-test-audit-impl"
    url = "https://github.com/dummy/fail-test-audit-impl/archive/v1.0.tar.gz"

    version("2.0", sha256="c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1")
    version("1.0", sha256="abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234")

    # The test method has not been implemented.
    def test_no_impl(self):
        """test sans implementation"""
        # this comment should not matter
        pass
