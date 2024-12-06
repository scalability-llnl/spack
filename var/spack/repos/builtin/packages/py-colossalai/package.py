# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColossalai(PythonPackage):
    """An integrated large-scale model training system with efficient
    parallelization techniques."""

    homepage = "https://www.colossalai.org/"
    pypi = "colossalai/colossalai-0.1.3.tar.gz"

    version("0.1.3", sha256="f25ffd313e62b2cb8f97c57f25fafb0e9f59ec7bd1d1bf6e8d8483f9b0082d33")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-torch@1.8:", type=("build", "run"))
    depends_on("py-torchvision@0.9:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-tensorboard", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-pre-commit", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"))
