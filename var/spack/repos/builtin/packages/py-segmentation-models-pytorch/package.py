# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySegmentationModelsPytorch(PythonPackage):
    """Python library with Neural Networks for Image Segmentation based on PyTorch."""

    homepage = "https://github.com/qubvel/segmentation_models.pytorch"
    pypi = "segmentation_models_pytorch/segmentation_models_pytorch-0.2.0.tar.gz"

    license("MIT")
    maintainers("adamjstewart")

    version("0.3.4", sha256="f4aee7f6add479bd3c3953e855b7055fc657dc6800bf7fc8ab733fd7f8acb163")
    version("0.3.3", sha256="b3b21ab4cd26a6b2b9e7a6ed466ace6452eb26ed3c31ae491ea2d7cbb01e384b")
    version("0.3.2", sha256="8372733e57a10cb8f6b9e18a20577fbb3fb83549b6945664dc774a9b6d3ecd13")
    version("0.3.1", sha256="d4a4817cf48872c3461bb7d22864c00f9d491719a6460adb252c035f9b0e8d51")
    version("0.3.0", sha256="8e00ed1707698d309d23f207aef15f21465e091aa0f1dc8043ec3300f5f67216")
    version("0.2.1", sha256="86744552b04c6bedf7e10f7928791894d8d9b399b9ed58ed1a3236d2bf69ead6")
    version("0.2.0", sha256="247266722c23feeef16b0862456c5ce815e5f0a77f95c2cd624a71bf00d955df")

    depends_on("py-setuptools", type="build")
    depends_on("py-torchvision@0.5.0:", type=("build", "run"))
    depends_on("py-pretrainedmodels@0.7.4", type=("build", "run"))
    depends_on("py-efficientnet-pytorch@0.7.1", when="@0.3:", type=("build", "run"))
    depends_on("py-efficientnet-pytorch@0.6.3", when="@:0.2", type=("build", "run"))
    depends_on("py-timm@0.9.7", when="@0.3.4", type=("build", "run"))
    depends_on("py-timm@0.9.2", when="@0.3.3", type=("build", "run"))
    depends_on("py-timm@0.6.12", when="@0.3.2", type=("build", "run"))
    depends_on("py-timm@0.4.12", when="@:0.3.1", type=("build", "run"))
    depends_on("py-huggingface-hub@0.24.6:", when="@0.3.4:", type=("build", "run"))
    depends_on("py-tqdm", when="@0.3:", type=("build", "run"))
    depends_on("pil", when="@0.3:", type=("build", "run"))
    depends_on("py-six", when="@0.3.4:", type=("build", "run"))
