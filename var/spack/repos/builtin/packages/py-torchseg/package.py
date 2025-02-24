# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchseg(PythonPackage):
    """TorchSeg: Semantic Segmentation models for PyTorch."""

    homepage = "https://github.com/isaaccorley/torchseg"
    pypi = "torchseg/torchseg-0.0.1a4.tar.gz"

    maintainers("isaaccorley", "adamjstewart")

    license("MIT")

    version("0.0.1a4", sha256="4742551753599af92f9f85e5ca6b149b474ffd458bad1aad6b3aad246a3bf4ea")

    depends_on("py-setuptools@61:")

    with default_args(type=("build", "run")):
        depends_on("py-einops@0.7:")
        depends_on("py-timm@0.9.12:")
        depends_on("py-torch@1.13:")
