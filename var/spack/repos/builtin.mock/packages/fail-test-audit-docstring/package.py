# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class FailTestAuditDocstring(MakefilePackage):
    """Simple package with a stand-alone test that is missing its docstring."""

    homepage = "http://github.com/dummy/fail-test-audit-docstring"
    url = "https://github.com/dummy/fail-test-audit-docstring/archive/v1.0.tar.gz"

    version("2.0", sha256="c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1")
    version("1.0", sha256="abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234")

    # The required docstring is missing.
    def test_missing_docstring(self):
        print("Ran test_missing_docstring")

    # The required docstring is effectively empty.
    def test_empty_docstring(self):
        """ """
        print("Ran test_empty_docstring")
