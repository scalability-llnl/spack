# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAutocfg(PythonPackage):
    """Deep learning configuration."""

    homepage = "https://github.com/zhreshold/autocfg"
    pypi = "autocfg/autocfg-0.0.8.tar.gz"

    version("0.0.8", sha256="749986b4f3b3bd85b15298734bf8fa4a590e6c34a314ac515025e058ed76c319")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml", type=("build", "run"))
