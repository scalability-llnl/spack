# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGluoncv(PythonPackage):
    """GluonCV provides implementations of state-of-the-art
    (SOTA) deep learning algorithms in computer vision. It aims
    to help engineers, researchers, and students quickly
    prototype products, validate new ideas and learn computer
    vision."""

    homepage = "https://gluon-cv.mxnet.io/"
    pypi = "gluoncv/gluoncv-0.6.0.tar.gz"
    git = "https://github.com/dmlc/gluon-cv.git"

    license("Apache-2.0")

    version(
        "0.10.5.post0", sha256="4598b9612e8b459a5a14ebeffedefcdae4a5700302a91f9b99fc82e9b08928a5"
    )
    version("0.6.0", sha256="313848b939c30e9e4c0040078421c02e32a350b8ebf2a966313fd893d7b3bdf6")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-portalocker", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-yacs", when="@0.8:", type=("build", "run"))
    depends_on("py-pandas", when="@0.9:", type=("build", "run"))
    depends_on("py-pyyaml", when="@0.9:", type=("build", "run"))
    depends_on("py-autocfg", when="@0.9:", type=("build", "run"))
