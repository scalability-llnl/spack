# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPretrainedmodels(PythonPackage):
    """Pretrained models for Pytorch."""

    homepage = "https://github.com/cadene/pretrained-models.pytorch"
    pypi = "pretrainedmodels/pretrainedmodels-0.7.4.tar.gz"

    version("0.7.4", sha256="7e77ead4619a3e11ab3c41982c8ad5b86edffe37c87fd2a37ec3c2cc6470b98a")

    depends_on("py-setuptools", type="build")
    depends_on("py-torch", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
    depends_on("py-munch", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
