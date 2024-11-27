# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPulp(PythonPackage):
    """PuLP is an LP modeler written in Python. PuLP can generate MPS or LP
    files and call GLPK, COIN-OR CLP/CBC, CPLEX, GUROBI, MOSEK, XPRESS, CHOCO,
    MIPCL, SCIP to solve linear problems."""

    homepage = "https://github.com/coin-or/pulp"
    pypi = "PuLP/PuLP-2.6.0.tar.gz"

    maintainers("marcusboden")

    license("MIT")

    version("2.6.0", sha256="4b4f7e1e954453e1b233720be23aea2f10ff068a835ac10c090a93d8e2eb2e8d")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
