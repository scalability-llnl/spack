# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocstringsPython(PythonPackage):
    """A Python handler for mkdocstrings."""

    homepage = "https://mkdocstrings.github.io/python/"
    pypi = "mkdocstrings-python/mkdocstrings-python-0.7.1.tar.gz"

    license("ISC")

    version("0.7.1", sha256="c334b382dca202dfa37071c182418a6df5818356a95d54362a2b24822ca3af71")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-pdm-pep517", type="build")
    depends_on("py-mkdocstrings@0.19:", type=("build", "run"))
    depends_on("py-griffe@0.11.1:", type=("build", "run"))
