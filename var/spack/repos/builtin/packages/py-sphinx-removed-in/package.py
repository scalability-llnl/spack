# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxRemovedIn(PythonPackage):
    """versionremoved and removed-in directives for Sphinx."""

    homepage = "https://github.com/MrSenko/sphinx-removed-in"
    pypi = "sphinx-removed-in/sphinx-removed-in-0.2.1.tar.gz"

    maintainers("LydDeb")

    version("0.2.1", sha256="0588239cb534cd97b1d3900d0444311c119e45296a9f73f1ea81ea81a2cd3db1")

    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx", type=("build", "run"))
