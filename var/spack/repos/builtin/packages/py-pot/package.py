# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPot(PythonPackage):
    """
    This open source Python library provide several solvers for optimization
    problems related to Optimal Transport for signal, image processing and
    machine learning.
    """

    homepage = "https://github.com/PythonOT/POT"
    pypi = "POT/POT-0.7.0.tar.gz"

    license("MIT")

    version("0.7.0", sha256="d4ac2bc8791f049a3166820d51e218d6c299885449b735eafef8d18c76d4ad06")

    depends_on("cxx", type="build")  # generated

    # Avoid that CC and CXX are overridden with g++ in setup.py.
    patch("175.patch", when="@0.7.0")

    depends_on("python@2.7.0:2.7,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.16:", type=("build", "run"))
    depends_on("py-scipy@1.0:", type=("build", "run"))
    depends_on("py-cython@0.23:", type=("build", "run"))
