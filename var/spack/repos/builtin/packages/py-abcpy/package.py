# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAbcpy(PythonPackage):
    """
    ABCpy is a highly modular, scientific library for approximate Bayesian
    computation (ABC) written in Python. It is designed to run all included ABC
    algorithms in parallel, either using multiple cores of a single computer or
    using an Apache Spark or MPI enabled cluster.
    """

    homepage = "https://github.com/eth-cscs/abcpy"
    pypi = "abcpy/abcpy-0.6.3.tar.gz"

    license("BSD-3-Clause-Clear")

    version("0.6.3", sha256="14cd959f3ccff8f5fd1d16239b8706cc8d1c1e2fe25d72855f500f005de41245")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn@0.23.1:", type=("build", "run"))
    depends_on("py-glmnet@2.2.1:", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-cloudpickle", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-pot", type=("build", "run"))

    # Development dependencies are required in setup.py :(
    depends_on("py-sphinx", type="build")
    depends_on("py-sphinx-rtd-theme", type="build")
    depends_on("py-coverage", type="build")
