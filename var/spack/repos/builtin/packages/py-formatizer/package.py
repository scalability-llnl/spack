# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFormatizer(PythonPackage):
    """Literal string formatting for Python versions older than 3.6."""

    homepage = "https://github.com/fgimian/formatizer"
    pypi = "formatizer/formatizer-0.1.1.tar.gz"

    license("MIT")

    version("0.1.1", sha256="3061ced1daa08f1836b79f4a3de16a33a54179331273e0b9c757d27ab339c29f")

    depends_on("py-setuptools", type="build")
