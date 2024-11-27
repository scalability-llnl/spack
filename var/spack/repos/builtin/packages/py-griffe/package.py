# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGriffe(PythonPackage):
    """Signatures for entire Python programs. Extract the structure, the frame,
    the skeleton of your project, to generate API documentation or find
    breaking changes in your API."""

    homepage = "https://mkdocstrings.github.io/griffe/"
    pypi = "griffe/griffe-0.22.0.tar.gz"

    license("ISC")

    version("0.22.0", sha256="a3c25a2b7bf729ecee7cd455b4eff548f01c620b8f58a8097a800caad221f12e")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-pdm-pep517", type="build")
    depends_on("py-cached-property", type=("build", "run"), when="^python@:3.7")
