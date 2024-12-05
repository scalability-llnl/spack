# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLocket(PythonPackage):
    """File-based locks for Python for Linux and Windows."""

    homepage = "https://github.com/mwilliamson/locket.py"
    pypi = "locket/locket-0.2.0.tar.gz"

    license("BSD-2-Clause")

    version("1.0.0", sha256="5c0d4c052a8bbbf750e056a8e65ccd309086f4f0f18a2eac306a8dfa4112a632")
    version("0.2.0", sha256="1fee63c1153db602b50154684f5725564e63a0f6d09366a1cb13dffcec179fb4")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
