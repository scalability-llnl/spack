# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAutodocsumm(PythonPackage):
    """Extended sphinx autodoc including automatic autosummaries."""

    homepage = "https://github.com/Chilipp/autodocsumm"
    pypi = "autodocsumm/autodocsumm-0.2.11.tar.gz"

    maintainers("LydDeb")

    license("Apache-2.0")

    version("0.2.11", sha256="183212bd9e9f3b58a96bb21b7958ee4e06224107aa45b2fd894b61b83581b9a9")

    depends_on("py-setuptools@61.0:", type="build")
    depends_on("py-versioneer+toml", type="build")
    depends_on("py-sphinx@2.2:7", type=("build", "run"))
