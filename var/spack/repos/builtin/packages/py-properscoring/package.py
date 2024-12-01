# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyProperscoring(PythonPackage):
    """Proper scoring rules in Python."""

    homepage = "https://github.com/properscoring/properscoring"
    pypi = "properscoring/properscoring-0.1.tar.gz"

    license("Apache-2.0")

    version("0.1", sha256="b0cc4963cc218b728d6c5f77b3259c8f835ae00e32e82678cdf6936049b93961")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
