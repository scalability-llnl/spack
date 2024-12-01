# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxBasicNg(PythonPackage):
    """A modern skeleton for Sphinx themes."""

    homepage = "https://github.com/pradyunsg/sphinx-basic-ng"
    pypi = "sphinx_basic_ng/sphinx_basic_ng-1.0.0b2.tar.gz"

    license("MIT")

    version("1.0.0b2", sha256="9ec55a47c90c8c002b5960c57492ec3021f5193cb26cebc2dc4ea226848651c9")

    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx@4:", type=("build", "run"))
