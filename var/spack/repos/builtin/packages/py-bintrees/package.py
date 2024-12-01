# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBintrees(PythonPackage):
    """Package provides Binary-, RedBlack- and AVL-Trees in Python and Cython."""

    homepage = "https://github.com/mozman/bintrees"
    pypi = "bintrees/bintrees-2.0.7.zip"

    version("2.0.7", sha256="60675e6602cef094abcd38bf4aecc067d78ae2d5e1645615c789724542d11270")

    depends_on("py-setuptools", type="build")
