# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDalib(PythonPackage):
    """Trans-Learn is a Transfer Learning library based on pure PyTorch with high
    performance and friendly API."""

    homepage = "https://github.com/thuml/Domain-Adaptation-Lib"
    pypi = "dalib/dalib-0.2.tar.gz"

    maintainers("meyersbs")

    version("0.2", sha256="3d06b37e4f93179f907d88a84d2d1802267bc397bf9cbd6bf5c69011bbae9a6a")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-torch@1.4.0:", type=("build", "run"))
    depends_on("py-torchvision@0.5.0:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-qpsolvers@1.4.0:", type=("build", "run"))
