# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCurvlinopsForPytorch(PythonPackage):
    """scipy Linear operators for curvature matrices in PyTorch."""

    homepage = "https://github.com/f-dangel/curvlinops"
    pypi = "curvlinops_for_pytorch/curvlinops_for_pytorch-2.0.0.tar.gz"

    license("MIT")

    version("2.0.0", sha256="01f9925db9454fc9b0a31c7b83fc8ec2534c2eb12b7de7825a5298fc14e460e7")

    with default_args(type="build"):
        depends_on("py-setuptools@61:")
        depends_on("py-setuptools-scm")

    with default_args(type=("build", "run")):
        depends_on("py-backpack-for-pytorch@1.6:1")
        depends_on("py-torch@2:")
        depends_on("py-scipy@1.7.1:1")
        depends_on("py-tqdm@4.61:4")
        depends_on("py-einops")
        depends_on("py-einconv")
