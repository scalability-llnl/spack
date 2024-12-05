# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocstrings(PythonPackage):
    """Automatic documentation from sources, for MkDocs."""

    homepage = "https://mkdocstrings.github.io/"
    pypi = "mkdocstrings/mkdocstrings-0.19.0.tar.gz"

    license("ISC")

    version("0.19.0", sha256="efa34a67bad11229d532d89f6836a8a215937548623b64f3698a1df62e01cc3e")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-pdm-pep517", type="build")
    depends_on("py-jinja2@2.11.1:", type=("build", "run"))
    depends_on("py-markdown@3.3:", type=("build", "run"))
    depends_on("py-markupsafe@1.1:", type=("build", "run"))
    depends_on("py-mkdocs@1.2:", type=("build", "run"))
    depends_on("py-mkdocs-autorefs@0.3.1:", type=("build", "run"))
    depends_on("py-pymdown-extensions@6.3:", type=("build", "run"))
