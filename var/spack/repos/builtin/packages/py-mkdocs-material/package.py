# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocsMaterial(PythonPackage):
    """Write your documentation in Markdown and create a professional static
    site for your Open Source or commercial project in minutes."""

    homepage = "https://squidfunk.github.io/mkdocs-material/"
    pypi = "mkdocs-material/mkdocs-material-8.4.0.tar.gz"

    license("MIT")

    version("8.4.0", sha256="6c0a6e6cda8b43956e0c562374588160af8110584a1444f422b1cfd91930f9c7")
    version("8.3.6", sha256="be8f95c0dfb927339b55b2cc066423dc0b381be9828ff74a5b02df979a859b66")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-jinja2@3.0.2:", type=("build", "run"))
    depends_on("py-markdown@3.2:", type=("build", "run"))
    depends_on("py-mkdocs@1.3.0:", type=("build", "run"))
    depends_on("py-mkdocs-material-extensions@1.0.3:", type=("build", "run"))
    depends_on("py-pygments@2.12:", type=("build", "run"))
    depends_on("py-pymdown-extensions@9.4:", type=("build", "run"))
