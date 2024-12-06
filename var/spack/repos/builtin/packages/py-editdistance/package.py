# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEditdistance(PythonPackage):
    """Fast implementation of the edit distance (Levenshtein distance)."""

    homepage = "https://github.com/aflc/editdistance"
    pypi = "editdistance/editdistance-0.4.tar.gz"
    git = "https://github.com/roy-ht/editdistance.git"

    maintainers("meyersbs")

    license("MIT")

    # PyPI tarball for version 0.6.2 missing bycython.pyx file
    # https://github.com/roy-ht/editdistance/issues/94#issuecomment-1426279375
    version("0.6.2", tag="v0.6.2", commit="3f5a5b0299f36662349df0917352a42c620e3dd4")
    version("0.4", sha256="c765db6f8817d38922e4a50be4b9ab338b2c539377b6fcf0bca11dea72eeb8c1")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-cython", when="@0.6.2:", type="build")
    depends_on("python@3.6:", when="@0.6.2:", type=("build", "run"))
