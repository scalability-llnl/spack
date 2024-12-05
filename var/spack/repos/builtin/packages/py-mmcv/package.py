# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMmcv(PythonPackage):
    """MMCV is a foundational python library for computer
    vision research and supports many research projects in
    MMLAB, such as MMDetection and MMAction."""

    homepage = "https://mmcv.readthedocs.io/en/latest/"
    url = "https://github.com/open-mmlab/mmcv/archive/v0.5.1.tar.gz"

    license("Apache-2.0")

    version("0.5.1", sha256="7c5ad30d9b61e44019e81ef46c406aa85dd08b5d0ba12ddd5cdc9c445835a55e")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-addict", type=("build", "run"))
    depends_on("py-numpy@1.11.1:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("opencv+python3", type=("build", "run"))
    depends_on("py-cython", type="build")

    patch("opencv_for0.5.1.patch", when="@0.5.1")
