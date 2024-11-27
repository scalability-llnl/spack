# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOcnn(PythonPackage):
    """O-CNN is an octree-based sparse convolutional neural network
    framework for 3D deep learning."""

    homepage = "https://github.com/octree-nn/ocnn-pytorch"
    pypi = "ocnn/ocnn-2.2.0.tar.gz"

    maintainers("wdconinc")

    license("MIT")

    version("2.2.0", sha256="5fb54305130921ece4cccf1697ec281f49d3e95837ba0e124cab9f8a567ecb80")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-torch@1.6.0:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
