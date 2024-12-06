# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEfficientnetPytorch(PythonPackage):
    """EfficientNet implemented in PyTorch."""

    homepage = "https://github.com/lukemelas/efficientnet_pytorch"
    pypi = "efficientnet_pytorch/efficientnet_pytorch-0.6.3.tar.gz"

    version("0.7.1", sha256="00b9b261effce59d2d47aae2ad238c29a2a65175470f41ada7ecac439b7c1ee1")
    version("0.6.3", sha256="6667459336893e9bf6367de3788ba449fed97f65da3b6782bf2204b6273a319f")

    depends_on("python@3.5.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-torch", type=("build", "run"))
