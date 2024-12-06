# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyts(PythonPackage):
    """pyts is a Python package for time series classification. It aims to make
    time series classification easily accessible by providing preprocessing and
    utility tools, and implementations of state-of-the-art algorithms. Most of
    these algorithms transform time series, thus pyts provides several tools to
    perform these transformations."""

    homepage = "https://github.com/johannfaouzi/pyts"
    pypi = "pyts/pyts-0.12.0.tar.gz"

    license("BSD-3-Clause")

    version("0.12.0", sha256="af85e09a14334cbe384318de6ca4379e9a30bf5bbd1aaf3a1c4a94872e9765b1")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.17.5:", type=("build", "run"))
    depends_on("py-scipy@1.3.0:", type=("build", "run"))
    depends_on("py-scikit-learn@0.22.1:", type=("build", "run"))
    depends_on("py-joblib@0.12:", type=("build", "run"))
    depends_on("py-numba@0.48.0:", type=("build", "run"))
