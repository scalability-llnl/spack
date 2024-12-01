# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFormulaic(PythonPackage):
    """Formulaic is a high-performance implementation of Wilkinson formulas
    for Python."""

    homepage = "https://github.com/matthewwardrop/formulaic"
    pypi = "formulaic/formulaic-0.2.4.tar.gz"

    version("0.6.1", sha256="5b20b2130436dc8bf5ea604e69d88d44b3be4d8ea20bfea96d982fa1f6bb762b")
    version("0.5.2", sha256="25b1e1c8dff73f0b11c0028a6ab350222de6bbc47b316ccb770cec16189cef53")
    version("0.2.4", sha256="15b71ea8972fb451f80684203cddd49620fc9ed5c2e35f31e0874e9c41910d1a")

    depends_on("python@3.7.2:", when="@5:", type=("build", "run"))
    depends_on("py-hatchling", when="@0.5:", type="build")
    depends_on("py-hatch-vcs", when="@0.5:", type="build")
    depends_on("py-setuptools", when="@:0.3.2", type="build")
    depends_on("py-setupmeta", when="@:0.3.2", type="build")

    depends_on("py-astor@0.8:", when="@0.3.4:", type=("build", "run"))
    depends_on("py-astor", type=("build", "run"))
    depends_on("py-cached-property@1.3:", when="@0.4: ^python@:3.7", type=("build", "run"))
    depends_on("py-graphlib-backport@1:", when="@0.5: ^python@:3.8", type=("build", "run"))
    depends_on("py-interface-meta@1.2:", type=("build", "run"))
    depends_on("py-numpy@1.16.5:", when="@0.5:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas@1:", when="@0.4:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-scipy@1.6:", when="@0.3:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-wrapt@1:", when="@0.3:", type=("build", "run"))
    depends_on("py-wrapt", type=("build", "run"))
    depends_on("py-typing-extensions@4.2:", when="@0.5:", type=("build", "run"))
