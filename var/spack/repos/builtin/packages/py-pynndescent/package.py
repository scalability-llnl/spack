# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPynndescent(PythonPackage):
    """PyNNDescent is a Python nearest neighbor descent for
    approximate nearest neighbors."""

    homepage = "https://github.com/lmcinnes/pynndescent"
    pypi = "pynndescent/pynndescent-0.5.7.tar.gz"

    license("BSD-2-Clause")

    version("0.5.7", sha256="ecb395255fa36a748b5870b4ba0300ea0f7da8b1964864b8edd62577a84dfd7d")

    depends_on("py-setuptools", type="build")
    depends_on("py-scikit-learn@0.18:", type=("build", "run"))
    depends_on("py-scipy@1.0:", type=("build", "run"))
    depends_on("py-numba@0.51.2:", type=("build", "run"))
    depends_on("py-llvmlite@0.30:", type=("build", "run"))
    depends_on("py-joblib@0.11:", type=("build", "run"))
