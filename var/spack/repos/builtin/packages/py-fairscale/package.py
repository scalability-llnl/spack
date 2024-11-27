# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFairscale(PythonPackage):
    """FairScale is a PyTorch extension library for high performance and large
    scale training. This library extends basic PyTorch capabilities while adding
    new SOTA scaling techniques."""

    homepage = "https://github.com/facebookresearch/fairscale"
    pypi = "fairscale/fairscale-0.4.13.tar.gz"

    license("Apache-2.0")

    version("0.4.13", sha256="1b797825c427f5dba92253fd0d8daa574e8bd651a2423497775fab1b30cfb768")
    version("0.4.4", sha256="7719898743dc58c04a2294c896ee6308c92ccb3af9e10632b2a62f77cb689357")

    variant("extra", default=False, description="support for cuda.list.gpu, scaler, weight")

    # from setup.py
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("ninja", type="build")
    # from pyproject.toml
    depends_on("py-wheel@0.30.0:", type="build")
    depends_on("py-setuptools@40.6.2:", type="build")
    # from requirements.txt
    depends_on("py-torch@1.8.0:", type=("build", "run"))
    depends_on("py-numpy@1.22.0:", type=("build", "run"))
    # added extra to support cuda.list.gpu, scaler, and weight (not in pip install)
    # see requirements-dev.txt in github. This does not include the tools for testing
    with when("+extra"):
        depends_on("py-pynvml@8.0.4", type=("build", "run"))
        depends_on("py-scikit-learn@1.1.3", type=("build", "run"))
        depends_on("py-pygit2@1.11.1", type=("build", "run"))
        depends_on("py-pgzip@0.3.1", type=("build", "run"))
