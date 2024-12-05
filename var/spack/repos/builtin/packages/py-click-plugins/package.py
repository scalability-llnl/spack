# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClickPlugins(PythonPackage):
    """An extension module for py-click to register external CLI
    commands via setuptools entry-points."""

    pypi = "click-plugins/click-plugins-1.0.4.tar.gz"

    license("BSD-3-Clause")

    version("1.1.1", sha256="46ab999744a9d831159c3411bb0c79346d94a444df9a3a3742e9ed63645f264b")
    version("1.0.4", sha256="dfed74b5063546a137de99baaaf742b4de4337ad2b3e1df5ec7c8a256adc0847")

    depends_on("py-setuptools", type="build")
    depends_on("py-click@3.0:", type=("build", "run"))
    depends_on("py-click@4.0:", type=("build", "run"), when="@1.1.1:")
