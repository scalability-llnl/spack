# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGenshi(PythonPackage):
    """Python toolkit for generation of output for the web"""

    pypi = "Genshi/Genshi-0.7.7.tar.gz"

    license("BSD-3-Clause")

    version("0.7.7", sha256="c100520862cd69085d10ee1a87e91289e7f59f6b3d9bd622bf58b2804e6b9aab")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-six", type=("build", "run", "test"))

    def test_testsuite(self):
        """run unittest suite"""
        python("-m", "unittest", "-v", "genshi.tests.suite")
