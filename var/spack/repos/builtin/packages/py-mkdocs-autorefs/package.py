# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocsAutorefs(PythonPackage):
    """Automatically link across pages in MkDocs."""

    homepage = "https://mkdocstrings.github.io/autorefs/"
    pypi = "mkdocs-autorefs/mkdocs-autorefs-0.4.1.tar.gz"

    license("ISC")

    version("0.4.1", sha256="70748a7bd025f9ecd6d6feeba8ba63f8e891a1af55f48e366d6d6e78493aba84")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-pdm-pep517", type="build")
    depends_on("py-markdown@3.3:", type=("build", "run"))
    depends_on("py-mkdocs@1.1:", type=("build", "run"))
