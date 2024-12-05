# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestArraydiff(PythonPackage):
    """pytest plugin to help with comparing array output from tests"""

    homepage = "https://github.com/astropy/pytest-arraydiff"
    pypi = "pytest-arraydiff/pytest-arraydiff-0.3.tar.gz"

    version("0.3", sha256="de2d62f53ecc107ed754d70d562adfa7573677a263216a7f19aa332f20dc6c15")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-pytest", type=("build", "run"))
