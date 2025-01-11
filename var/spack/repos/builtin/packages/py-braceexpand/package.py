# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyBraceexpand(PythonPackage):
    """Bash-style brace expansion"""

    homepage = "https://github.com/trendels/braceexpand"
    url = "https://github.com/trendels/braceexpand/archive/refs/tags/v0.1.7.tar.gz"

    license("MIT")

    version("0.1.7", sha256="72eb91b62b2fa2dd7f6044b7a4b46a3761ac61fe5945a2a86a4538447ab47e05")

    # Requires py-typing with python@:3.4 but Spack's minimum python is higher
    depends_on("py-setuptools")

    @run_after("install")
    def copy_test_files(self):
        cache_extra_test_sources(self, "test_braceexpand.py")

    def test_unittests(self):
        """run the unit tests"""
        with working_dir(self.test_suite.current_test_cache_dir):
            python("test_braceexpand.py")
