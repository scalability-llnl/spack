# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyscipopt(PythonPackage):
    """Python interface for the SCIP Optimization Suite"""

    homepage = "https://github.com/scipopt/PySCIPOpt"
    pypi = "PySCIPOpt/PySCIPOpt-3.4.0.tar.gz"

    license("MIT")

    version("3.4.0", sha256="8da4db57b21010e0d5a863292dd455c88dd71ecec12a8439171c213a8092f88a")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-wheel", type="build")
    depends_on("scipoptsuite")
