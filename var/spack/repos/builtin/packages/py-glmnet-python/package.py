# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGlmnetPython(PythonPackage):
    """This is a python version of the popular glmnet library (beta release).
    Glmnet fits the entire lasso or elastic-net regularization path for linear
    regression, logistic and multinomial regression models, poisson regression
    and the cox model."""

    # Not to be confused with py-glmnet

    homepage = "https://github.com/johnlees/glmnet_python/"
    # Not availible on PyPI. Note that this is a fork of
    # https://github.com/bbalasub1/glmnet_python, as required for py-pyseer
    url = "https://github.com/johnlees/glmnet_python/archive/v1.0.2.zip"

    version("1.0.2", sha256="cc80020dcebc5366dcc061aec59318efac69d23578066326d925bfc27a23cb27")

    depends_on("py-setuptools", type="build")
    depends_on("py-joblib@0.10.3:", type=("build", "run"))
    # Not in setup.py, but imported and used:
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
