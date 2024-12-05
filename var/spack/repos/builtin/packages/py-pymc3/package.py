# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPymc3(PythonPackage):
    """PyMC3 is a Python package for Bayesian statistical modeling and
    Probabilistic Machine Learning focusing on advanced Markov chain Monte
    Carlo (MCMC) and variational inference (VI) algorithms. Its flexibility and
    extensibility make it applicable to a large suite of problems."""

    homepage = "https://github.com/pymc-devs/pymc3"
    pypi = "pymc3/pymc3-3.8.tar.gz"

    license("Apache-2.0")

    version("3.8", sha256="1bb2915e4a29877c681ead13932b0b7d276f7f496e9c3f09ba96b977c99caf00")

    depends_on("python@3.5.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-arviz@0.4.1:", type=("build", "run"))
    depends_on("py-theano@1.0.4:", type=("build", "run"))
    depends_on("py-numpy@1.13.0:", type=("build", "run"))
    depends_on("py-scipy@0.18.1:", type=("build", "run"))
    depends_on("py-pandas@0.18.0:", type=("build", "run"))
    depends_on("py-patsy@0.4.0:", type=("build", "run"))
    depends_on("py-tqdm@4.8.4:", type=("build", "run"))
    depends_on("py-h5py@2.7.0:", type=("build", "run"))
