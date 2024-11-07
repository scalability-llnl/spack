# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightningUqBox(PythonPackage):
    """Lighning-UQ-Box: A toolbox for uncertainty quantification in deep learning."""

    homepage = "https://github.com/lightning-uq-box/lightning-uq-box"
    pypi = "lightning-uq-box/lightning-uq-box-0.1.0.tar.gz"
    git = "https://github.com/lightning-uq-box/lightning-uq-box.git"

    license("Apache-2.0")
    maintainers("nilsleh", "adamjstewart")

    version("main", branch="main")
    version("0.1.0", sha256="ce44860db75b4fbe487a009bee91c886be2e1835edee93479a6a8633ef2152b1")

    depends_on("py-setuptools@61:", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:", when="@0.2:")
        depends_on("python@3.9:")
        depends_on("py-einops@0.3:")
        depends_on("py-lightning@2.4:", when="@0.2:")
        depends_on("py-lightning@2.1.1:")
        depends_on("py-matplotlib@3.5:", when="@0.2:")
        depends_on("py-matplotlib@3.3.3:")
        depends_on("py-numpy@1.21.1:", when="@0.2:")
        depends_on("py-numpy@1.19.3:")
        depends_on("py-pandas@1.1.3:")
        depends_on("py-torch@2:")
        depends_on("py-torchmetrics@1.2:")
        depends_on("py-torchvision@0.16.1:")
        depends_on("py-scikit-learn@1.3:")
        depends_on("py-gpytorch@1.11:")
        depends_on("py-laplace-torch@0.2.1:", when="@0.2:")
        depends_on("py-laplace-torch@0.1:")
        depends_on("py-uncertainty-toolbox@0.1.1:")
        depends_on("py-kornia@0.6.9:")
        depends_on("py-timm@0.9.2:")
        depends_on("py-torchseg@0.0.1:")
        depends_on("py-h5py@3.12.1:", when="@0.2:")
        depends_on("py-ema-pytorch@0.7:", when="@0.2:")
