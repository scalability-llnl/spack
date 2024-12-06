# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDunamai(PythonPackage):
    """Dynamic version generation."""

    homepage = "https://github.com/mtkennerly/dunamai"
    pypi = "dunamai/dunamai-1.13.1.tar.gz"

    license("MIT")

    version("1.18.0", sha256="5200598561ea5ba956a6174c36e402e92206c6a6aa4a93a6c5cb8003ee1e0997")
    version("1.17.0", sha256="459381b585a1e78e4070f0d38a6afb4d67de2ee95064bf6b0438ec620dde0820")
    version("1.13.1", sha256="49597bdf653bdacdeb51ec6e0f1d4d2327309376fc83e6f1d42af6e29600515f")

    depends_on("python@3.5:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")

    depends_on("py-packaging@20.9:", type=("build", "run"))
    depends_on("py-importlib-metadata@1.6:", when="^python@:3.7", type=("build", "run"))
