# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribNapoleon(PythonPackage):
    """Sphinx "napoleon" extension."""

    homepage = "https://github.com/sphinx-contrib/napoleon"
    pypi = "sphinxcontrib-napoleon/sphinxcontrib-napoleon-0.7.tar.gz"

    license("BSD-2-Clause")

    version("0.7", sha256="407382beed396e9f2d7f3043fad6afda95719204a1e1a231ac865f40abcbfcf8")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.5.2:", type=("build", "run"))
    depends_on("py-pockets@0.3:", type=("build", "run"))
