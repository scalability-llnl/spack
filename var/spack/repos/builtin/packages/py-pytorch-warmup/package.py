# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytorchWarmup(PythonPackage):
    """This library contains PyTorch implementations of the warmup schedules
    described in On the adequacy of untuned warmup for adaptive
    optimization."""

    homepage = "https://github.com/Tony-Y/pytorch_warmup"
    pypi = "pytorch-warmup/pytorch-warmup-0.1.1.tar.gz"

    license("MIT", checked_by="alex391")

    version("0.1.1", sha256="c594760b29657a127aa6a8c3424dd0b5068140b3b7d4988118f4a9f3e99b1457")

    depends_on("py-setuptools", type="build")
    depends_on("py-torch@1.1:", type=("build", "run"))
