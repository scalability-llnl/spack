# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRepozeLru(PythonPackage):
    """A tiny LRU cache implementation and decorator"""

    pypi = "repoze.lru/repoze.lru-0.7.tar.gz"

    version("0.7", sha256="0429a75e19380e4ed50c0694e26ac8819b4ea7851ee1fc7583c8572db80aff77")

    variant("docs", default=False, description="Build docs")

    depends_on("py-setuptools", type="build")
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-sphinx", type="build", when="+docs")
