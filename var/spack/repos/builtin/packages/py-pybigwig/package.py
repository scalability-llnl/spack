# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPybigwig(PythonPackage):
    """A package for accessing bigWig files using libBigWig."""

    pypi = "pyBigWig/pyBigWig-0.3.4.tar.gz"

    license("MIT")

    version("0.3.12", sha256="e01991790ece496bf6d3f00778dcfb136dd9ca0fd28acc1b3fb43051ad9b8403")
    version("0.3.4", sha256="8c97a19218023190041c0e426f1544f7a4944a7bb4568faca1d85f1975af9ee2")

    depends_on("c", type="build")  # generated

    variant("numpy", default=True, description="Enable support for numpy integers and vectors")

    patch("python3_curl.patch", when="@:0.3.12 ^python@3:")

    depends_on("curl", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"), when="+numpy")
