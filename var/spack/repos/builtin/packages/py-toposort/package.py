# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyToposort(PythonPackage):
    """Implements a topological sort algorithm."""

    pypi = "toposort/toposort-1.10.tar.gz"

    maintainers("marcusboden")

    license("Apache-2.0")

    version("1.10", sha256="bfbb479c53d0a696ea7402601f4e693c97b0367837c8898bc6471adfca37a6bd")
    version("1.9", sha256="f41a34490d44934b533a7bdaff979ee8a47203fd2d8a746db83f2d5ab12458b9")
    version("1.8", sha256="b1e89996c43daaf0e03805d33df22333c99c9d36715b188dea0e551ce2f1cd81")
    version("1.7", sha256="ddc2182c42912a440511bd7ff5d3e6a1cabc3accbc674a3258c8c41cbfbb2125")
    version("1.6", sha256="a7428f56ef844f5055bb9e9e44b343983773ae6dce0fe5b101e08e27ffbd50ac")

    depends_on("python@3.8:", type=("build", "run"), when="@1.8:")
    depends_on("python@2.7:2.8,3.3:", type=("build", "run"), when="@:1.8")

    depends_on("py-setuptools@42:", type="build", when="@1.7:")
    depends_on("py-setuptools", type="build")
