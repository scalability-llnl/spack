# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMeautility(PythonPackage):
    """Python package for multi-electrode array (MEA) handling and stimulation."""

    homepage = "https://github.com/alejoe91/MEAutility"
    pypi = "meautility/MEAutility-1.5.1.tar.gz"

    license("GPL-3.0-or-later")

    version("1.5.1", sha256="de12cc9c1772d3321e941af78e6bfb36cdcb5702a7b1272a852cc95f413bbfcb")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
