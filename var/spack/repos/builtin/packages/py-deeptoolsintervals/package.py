# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeeptoolsintervals(PythonPackage):
    """A python module creating/accessing GTF-based interval trees with
    associated meta-data."""

    pypi = "deeptoolsintervals/deeptoolsintervals-0.1.9.tar.gz"

    license("MIT")

    version("0.1.9", sha256="7d94c36fd2b6f10d8b99e536d2672e8228971f1fc810497d33527bba2c40d4f6")

    depends_on("c", type="build")  # generated

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
