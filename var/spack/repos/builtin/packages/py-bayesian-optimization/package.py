# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBayesianOptimization(PythonPackage):
    """Pure Python implementation of bayesian global
    optimization with gaussian processes."""

    homepage = "https://github.com/fmfn/BayesianOptimization"
    pypi = "bayesian-optimization/bayesian-optimization-1.2.0.tar.gz"

    version("1.2.0", sha256="c2fd3af4b6cc24ee1c145295b2a900ffb9b455cad924e8185a8d5784712bc935")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.9.0:", type=("build", "run"))
    depends_on("py-scipy@0.14.0:", type=("build", "run"))
    depends_on("py-scikit-learn@0.18.0:", type=("build", "run"))
