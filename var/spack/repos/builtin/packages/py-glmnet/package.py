# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGlmnet(PythonPackage):
    """
    This is a Python wrapper for the fortran library used in the R package
    glmnet.
    """

    homepage = "https://github.com/civisanalytics/python-glmnet"
    pypi = "glmnet/glmnet-2.2.1.tar.gz"

    license("GPL-2.0-only")

    version("2.2.1", sha256="3222bca2e901b3f60c2dc22df7aeba6bb9c7b6451b44cbbe1b91084b66f14481")

    depends_on("fortran", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))

    depends_on("py-numpy@1.9.2:", type=("build", "run"))
    depends_on("py-scikit-learn@0.18.0:", type=("build", "run"))
    depends_on("py-scipy@0.14.1:", type=("build", "run"))
    depends_on("py-joblib@0.14.1:", type=("build", "run"))
