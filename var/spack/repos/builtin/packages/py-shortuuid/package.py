# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyShortuuid(PythonPackage):
    """A generator library for concise, unambiguous and URL-safe UUIDs."""

    homepage = "https://github.com/skorokithakis/shortuuid"
    url = "https://github.com/skorokithakis/shortuuid/archive/v1.0.0.tar.gz"

    license("BSD-3-Clause")

    version("1.0.11", sha256="6ba28eece88d23389684585d73f3d883be3a76d6ab0c5d18ef34e5de2d500d0f")
    version("1.0.1", sha256="1253bdddf0d866e0bd8ea70989702772e09a78d5072b0490dfb6b3489750c157")
    version("1.0.0", sha256="cc2539aaed1b4de34853ee4aaf8331176b768a2d3a87d5a790453e082ce36850")
    version("0.5.0", sha256="5dabb502352a43f67284a0edb16a1d46ec9f71b332df2095218c2df1be7d019c")

    depends_on("python@2.5:", type=("build", "run"), when="@:1.0.0")
    depends_on("python@3.5:", type=("build", "run"), when="@1.0.1:")
    depends_on("py-setuptools", type="build", when="@:1.0.8")
    depends_on("py-poetry-core", type="build", when="@1.0.9:")
