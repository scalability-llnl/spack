# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytimeparse(PythonPackage):
    """A small Python library to parse various kinds of time expressions."""

    homepage = "https://github.com/wroberts/pytimeparse"
    pypi = "pytimeparse/pytimeparse-1.1.8.tar.gz"

    license("MIT")

    version("1.1.8", sha256="e86136477be924d7e670646a98561957e8ca7308d44841e21f5ddea757556a0a")

    depends_on("py-setuptools", type="build")
