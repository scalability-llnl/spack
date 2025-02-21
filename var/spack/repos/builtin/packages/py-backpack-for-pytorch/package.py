# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackpackForPytorch(PythonPackage):
    """BackPACK: Packing more into backprop."""

    homepage = "https://github.com/f-dangel/backpack"
    pypi = "backpack-for-pytorch/backpack-for-pytorch-1.6.0.tar.gz"

    license("MIT")

    version("1.6.0", sha256="af6495b71bacf82a1c7cab01aa85bebabccfe74d87d89f108ea72a4a0d384de3")

    with default_args(type="build"):
        depends_on("py-setuptools@38.3:")
        depends_on("py-setuptools-scm")

    with default_args(type=("build", "run")):
        depends_on("py-torch@1.9:")
        depends_on("py-torchvision@0.7:")
        depends_on("py-einops@0.3:0")
        depends_on("py-unfoldnd@0.2:0")
