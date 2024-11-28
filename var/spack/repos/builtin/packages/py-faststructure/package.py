# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFaststructure(PythonPackage):
    """FastStructure is a fast algorithm for inferring population structure
    from large SNP genotype data."""

    homepage = "https://github.com/rajanil/fastStructure"
    url = "https://github.com/rajanil/fastStructure/archive/v1.0.tar.gz"

    license("MIT")

    version("1.0", sha256="f1bfb24bb5ecd108bc3a90145fad232012165c1e60608003f1c87d200f867b81")

    depends_on("c", type="build")  # generated

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("gsl")
