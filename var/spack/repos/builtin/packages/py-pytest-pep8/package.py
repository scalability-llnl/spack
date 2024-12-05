# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestPep8(PythonPackage):
    """pytest plugin for efficiently checking PEP8 compliance"""

    pypi = "pytest-pep8/pytest-pep8-1.0.6.tar.gz"

    license("MIT")

    version("1.0.6", sha256="032ef7e5fa3ac30f4458c73e05bb67b0f036a8a5cb418a534b3170f89f120318")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest-cache", type=("build", "run"))
    depends_on("py-pytest@2.4.2:", type=("build", "run"))
    depends_on("py-pep8@1.3:", type=("build", "run"))
