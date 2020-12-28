# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPyamg(PythonPackage):
    """PyAMG is a library of Algebraic Multigrid (AMG) solvers with
    a convenient Python interface."""

    homepage = "https://github.com/pyamg/pyamg"
    url      = "https://github.com/pyamg/pyamg/archive/v4.0.0.zip"

    # A list of GitHub accounts to notify when the package is updated.
    maintainers = ['benc303']

    version('4.0.0', sha256="015d5e706e6e54d3de82e05fdb173c30d8b27cb8a117ab584cd62ad41d9ea042")

    # Dependencies. A generic python dependency is added implicity by the
    # PythonPackage class.
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
