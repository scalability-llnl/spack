# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReadmeRenderer(PythonPackage):
    """readme_renderer is a library for rendering "readme" descriptions
    for Warehouse."""

    homepage = "https://github.com/pypa/readme_renderer"
    pypi = "readme_renderer/readme_renderer-24.0.tar.gz"

    version("37.3", sha256="cd653186dfc73055656f090f227f5cb22a046d7f71a841dfa305f55c9a513273")
    version("24.0", sha256="bb16f55b259f27f75f640acf5e00cf897845a8b3e4731b5c1a436e4b8529202f")
    version("16.0", sha256="c46b3418ddef3c3c3f819a4a9cfd56ede15c03d12197962a7e7a89edf1823dd5")

    depends_on("python@3.7:", when="@35:", type=("build", "run"))
    depends_on("py-setuptools@40.8:", when="@33:", type="build")
    depends_on("py-setuptools", type="build")

    depends_on("py-bleach@2.1.0:", type=("build", "run"))
    depends_on("py-docutils@0.13.1:", type=("build", "run"))
    depends_on("py-pygments@2.5.1:", when="@25:", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-six", when="@:29", type=("build", "run"))
