# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxMultiversion(PythonPackage):
    """A Sphinx extension for building self-hosted versioned documentation."""

    homepage = "https://github.com/Holzhaus/sphinx-multiversion"
    pypi = "sphinx-multiversion/sphinx-multiversion-0.2.4.tar.gz"

    version("0.2.4", sha256="5cd1ca9ecb5eed63cb8d6ce5e9c438ca13af4fa98e7eb6f376be541dd4990bcb")
    version("0.2.3", sha256="e46565ac2f703f3b55652f33c159c8059865f5d13dae7f0e8403e5afc2996f5f")
    version("0.2.2", sha256="c0a4f2cbb13eb62b5cd79e2f6901e5d90ea191d3f37e96e1f15b976827de0ac0")
    version("0.2.1", sha256="0775847454965005a3a8433c1bf38379f723c026de9c4a7ddd447b0349df90c1")

    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx", type=("build", "run"))
