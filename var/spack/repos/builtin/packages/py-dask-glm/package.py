# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDaskGlm(PythonPackage):
    """Dask-glm is a library for fitting Generalized Linear Models on
    large datasets."""

    homepage = "https://dask-glm.readthedocs.io/en/latest/"
    pypi = "dask-glm/dask-glm-0.2.0.tar.gz"

    license("BSD-3-Clause")

    version("0.2.0", sha256="58b86cebf04fe5b9e58092e1c467e32e60d01e11b71fdc628baaa9fc6d1adee5")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-cloudpickle@0.2.2:", type=("build", "run"))
    depends_on("py-dask+array", type=("build", "run"))
    depends_on("py-multipledispatch@0.4.9:", type=("build", "run"))
    depends_on("py-scipy@0.18.1:", type=("build", "run"))
    depends_on("py-scikit-learn@0.18:", type=("build", "run"))
