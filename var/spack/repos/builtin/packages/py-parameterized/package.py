# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParameterized(PythonPackage):
    """Parameterized testing with any Python test framework."""

    homepage = "https://github.com/wolever/parameterized"
    pypi = "parameterized/parameterized-0.7.1.tar.gz"

    version("0.7.1", sha256="6a94dbea30c6abde99fd4c2f2042c1bf7f980e48908bf92ead62394f93cf57ed")

    depends_on("py-setuptools", type="build")
