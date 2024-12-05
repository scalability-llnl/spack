# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocsJupyter(PythonPackage):
    """Use Jupyter in mkdocs websites."""

    homepage = "https://github.com/danielfrg/mkdocs-jupyter"
    pypi = "mkdocs-jupyter/mkdocs-jupyter-0.21.0.tar.gz"

    license("Apache-2.0")

    version("0.21.0", sha256="c8c00ce44456e3cf50c5dc3fe0cb18fab6467fb5bafc2c0bfe1efff3e0a52470")
    version("0.20.1", sha256="3b6ef675ee2f22ad94047db7f84e212f5278529df659f7584b5a2b8662db39f6")

    depends_on("python@3.7.1:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-setuptools@57.0:57", type="build")
    depends_on("py-nbconvert@6.2:6", type=("build", "run"))
    depends_on("py-jupytext@1.13.8:1", type=("build", "run"), when="@0.21.0:")
    depends_on("py-jupytext@1.11.02:1", type=("build", "run"), when="@:0.20")
    depends_on("py-mkdocs@1.2.3:1", type=("build", "run"))
    depends_on("py-mkdocs-material@8.0:8", type=("build", "run"))
    depends_on("py-pygments@2.12.0:2", type=("build", "run"), when="@0.21.0:")
