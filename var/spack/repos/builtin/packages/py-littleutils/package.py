# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLittleutils(PythonPackage):
    """Small personal collection of python utility functions, partly just for
    fun."""

    homepage = "https://github.com/alexmojaki/littleutils"
    pypi = "littleutils/littleutils-0.2.2.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("0.2.2", sha256="e6cae3a4203e530d51c9667ed310ffe3b1948f2876e3d69605b3de4b7d96916f")

    depends_on("py-setuptools", type="build")
