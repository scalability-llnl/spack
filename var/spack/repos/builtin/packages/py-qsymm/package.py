# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQsymm(PythonPackage):
    """Qsymm is a symmetry finder and symmetric Hamiltonian generator.
    It automatically generates model Hamiltonians from symmetry
    constraints and finds the full symmetry group of your Hamiltonian."""

    homepage = "https://gitlab.kwant-project.org/qt/qsymm"
    pypi = "qsymm/qsymm-1.2.7.tar.gz"
    git = "https://gitlab.kwant-project.org/qt/qsymm.git"

    # Add a list of GitHub accounts to notify when the
    # package is updated
    maintainers("payerle")

    license("BSD-2-Clause")

    version("1.2.7", sha256="9af92a30c3f72883c744d4717e4ec30c8b48121e208c10553e8e0e428fe43bbc")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.13:", type=("build", "run"))
    depends_on("py-scipy@0.19:", type=("build", "run"))
    depends_on("py-sympy@1.1:", type=("build", "run"))
    depends_on("py-tinyarray", type=("build", "run"))
    depends_on("py-pytest-runner", type="build")
