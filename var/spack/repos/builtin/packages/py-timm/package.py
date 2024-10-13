# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTimm(PythonPackage):
    """(Unofficial) PyTorch Image Models."""

    homepage = "https://github.com/rwightman/pytorch-image-models"
    pypi = "timm/timm-0.4.12.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version("0.9.7", sha256="2bfb1029e90b72e65eb9c75556169815f2e82257eaa1f6ebd623a4b4a52867a2")
    version("0.9.5", sha256="669835f0030cfb2412c464b7b563bb240d4d41a141226afbbf1b457e4f18cff1")
    version("0.9.2", sha256="d0977cc5e02c69bda979fca8b52aa315a5f2cb64ebf8ad2c4631b1e452762c14")
    version("0.9.1", sha256="171420ac499e7999d38fb8b08fffa5ca3950b38db23bba84763cd92621ca80a2")
    version("0.9.0", sha256="f0159bbeea5c8d11551ac3077752ee77008d2638578571303296054b5ffddad4")
    version("0.6.13", sha256="745c54f7b7985a18e08bd66c997b018c1c3fef99bbb8c018879a6f85571782f5")
    version("0.6.12", sha256="8f1747121598e06a1ea2d00df16d332cc284cdd4596bdc136b490a2122d3aa91")
    version("0.5.4", sha256="5d7b92e66a76c432009aba90d515ea7a882aae573415a7c5269e3617df901c1f")
    version("0.4.12", sha256="b14be70dbd4528b5ca8657cf5bc2672c7918c3d9ebfbffe80f4785b54e884b1e")

    # https://github.com/huggingface/pytorch-image-models/commit/f744bda994ec305a823483bf52a20c1440205032
    depends_on("python@3.8:", when="@0.9.0", type=("build", "run"))
    # https://github.com/huggingface/pytorch-image-models/issues/1530
    # https://github.com/huggingface/pytorch-image-models/pull/1649
    depends_on("python@:3.10", when="@:0.6.12", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-torch@1.7:", when="@0.6:", type=("build", "run"))
    depends_on("py-torch@1.4:", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
    depends_on("py-pyyaml", when="@0.6:", type=("build", "run"))
    depends_on("py-huggingface-hub", when="@0.6:", type=("build", "run"))
    depends_on("py-safetensors", when="@0.9:", type=("build", "run"))

    # https://github.com/rwightman/pytorch-image-models/pull/1256
    depends_on("pil@:9", when="@:0.5", type=("build", "run"))
    depends_on("py-numpy", when="@:0.5", type=("build", "run"))
