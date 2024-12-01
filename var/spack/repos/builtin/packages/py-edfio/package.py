# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEdfio(PythonPackage):
    """Read and write EDF/EDF+ files."""

    homepage = "https://github.com/the-siesta-group/edfio"
    pypi = "edfio/edfio-0.4.3.tar.gz"
    git = "https://github.com/the-siesta-group/edfio"

    license("Apache-2.0")

    version("0.4.3", sha256="9250e67af190379bb3432356b23c441a99682e97159ea58d4507b0827175b487")

    depends_on("python@3.9:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-poetry-dynamic-versioning@1", type="build")

    depends_on("py-numpy@1.22.0:", type=("build", "run"))
