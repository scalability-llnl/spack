# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWinUnicodeConsole(PythonPackage):
    """Enable Unicode input and display when running Python from Windows
    console."""

    homepage = "https://github.com/Drekin/win-unicode-console"
    pypi = "win_unicode_console/win_unicode_console-0.5.zip"

    version("0.5", sha256="d4142d4d56d46f449d6f00536a73625a871cba040f0bc1a2e305a04578f07d1e")

    depends_on("py-setuptools", type="build")
