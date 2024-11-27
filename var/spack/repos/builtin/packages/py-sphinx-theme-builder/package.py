# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxThemeBuilder(PythonPackage):
    """A tool for authoring Sphinx themes with a simple (opinionated) workflow."""

    homepage = "https://sphinx-theme-builder.readthedocs.io/en/latest"
    pypi = "sphinx-theme-builder/sphinx-theme-builder-0.2.0b2.tar.gz"
    git = "https://github.com/pradyunsg/sphinx-theme-builder"

    license("MIT")

    version("0.2.0b2", sha256="e9cd98c2bb35bf414fe721469a043cdcc10f0808d1ffcf606acb4a6282a6f288")

    depends_on("py-flit-core@3.2:3", type="build")

    depends_on("py-pyproject-metadata", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"))
    depends_on("py-nodeenv", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-tomli", when="^python@:3.10", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))
