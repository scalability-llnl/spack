# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLaplaceTorch(PythonPackage):
    """laplace - Laplace approximations for deep learning."""

    homepage = "https://github.com/aleximmer/Laplace"
    pypi = "laplace_torch/laplace_torch-0.2.1.tar.gz"

    license("MIT")

    version("0.2.1", sha256="641823a6d3e1dcb8297202b896ae2969334bf96df9a4a6f8cf688896d67d96f2")

    with default_args(type="build"):
        depends_on("py-setuptools@42:")
        depends_on("py-setuptools-scm")

    with default_args(type=("build", "run")):
        depends_on("py-torch@2:")
        depends_on("py-torchvision")
        depends_on("py-torchaudio")
        depends_on("py-backpack-for-pytorch")
        depends_on("py-asdfghjkl@0.1a4")
        depends_on("py-torchmetrics")
        depends_on("py-opt-einsum")
        depends_on("py-curvlinops-for-pytorch@2:")
