# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySmac(PythonPackage):
    """SMAC is a tool for algorithm configuration to optimize
    the parameters of arbitrary algorithms, including
    hyperparameter optimization of Machine Learning
    algorithms."""

    homepage = "https://automl.github.io/SMAC3/master/"
    pypi = "smac/smac-1.1.1.tar.gz"

    license("BSD-3-Clause")

    version("1.1.1", sha256="7b8c14c53384b32feb357b9f918a9b023cb01cbda2033e69125dee69ec0bd5b1")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.7.1:", type=("build", "run"))
    depends_on("py-scipy@1.7.0:", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pynisher@0.4.1:", type=("build", "run"))
    depends_on("py-configspace@0.4.14:0.4", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-scikit-learn@0.22.0:", type=("build", "run"))
    depends_on("py-pyrfr@0.8.0:", type=("build", "run"))
    depends_on("py-dask", type=("build", "run"))
    depends_on("py-distributed", type=("build", "run"))
    depends_on("py-emcee@3.0.0:", type=("build", "run"))
