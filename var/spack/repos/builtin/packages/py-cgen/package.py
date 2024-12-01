# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCgen(PythonPackage):
    """cgen offers a simple abstract syntax tree for C and related languages
    (C++/CUDA/OpenCL) to allow structured code generation from Python.
    """

    homepage = "https://documen.tician.de/cgen/"
    pypi = "cgen/cgen-2020.1.tar.gz"

    license("MIT")

    version("2020.1", sha256="4ec99d0c832d9f95f5e51dd18a629ad50df0b5464ce557ef42c6e0cd9478bfcf")

    depends_on("py-pytools@2015.1.2:", type=("build", "run"))
    depends_on("py-numpy@1.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
