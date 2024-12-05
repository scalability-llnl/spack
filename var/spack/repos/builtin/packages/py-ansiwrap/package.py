# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnsiwrap(PythonPackage):
    """textwrap, but savvy to ANSI colors and styles."""

    homepage = "https://github.com/jonathaneunice/ansiwrap"
    pypi = "ansiwrap/ansiwrap-0.8.4.zip"

    license("Apache-2.0")

    version("0.8.4", sha256="ca0c740734cde59bf919f8ff2c386f74f9a369818cdc60efe94893d01ea8d9b7")

    depends_on("py-setuptools", type="build")
    depends_on("py-textwrap3@0.9.2:", type=("build", "run"))
