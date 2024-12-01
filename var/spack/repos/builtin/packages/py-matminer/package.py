# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMatminer(PythonPackage):
    """Matminer is a library for performing data mining in the field of
    materials science."""

    homepage = "https://github.com/hackingmaterials/matminer"
    pypi = "matminer/matminer-0.8.0.tar.gz"

    maintainers("meyersbs")

    version("0.8.0", sha256="4bfc3dd6314720df6755cb1c38cad65995f9d820575296fcc67313a0a40c5747")

    depends_on("py-setuptools@43.0.0:", type="build")
    depends_on("py-numpy@1.20.1:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-pymongo", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-sympy", type=("build", "run"))
    depends_on("py-monty", type=("build", "run"))
    depends_on("py-pymatgen", type=("build", "run"))
