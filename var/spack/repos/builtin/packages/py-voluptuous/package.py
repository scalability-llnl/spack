# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVoluptuous(PythonPackage):
    """Voluptous, despite the name, is a Python data validation library."""

    homepage = "https://github.com/alecthomas/voluptuous"
    pypi = "voluptuous/voluptuous-0.11.5.tar.gz"

    license("BSD-3-Clause")

    version("0.11.7", sha256="2abc341dbc740c5e2302c7f9b8e2e243194fb4772585b991931cb5b22e9bf456")
    version("0.11.6", sha256="d2ca99ae1d1ed0313e8965720d1d75a780fc7f312fea4e3dbbb56ccfe5a8306d")
    version("0.11.5", sha256="567a56286ef82a9d7ae0628c5842f65f516abcb496e74f3f59f1d7b28df314ef")

    depends_on("py-setuptools", type="build")
