# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDesc(RPackage):
    """Manipulate DESCRIPTION Files.

    Tools to read, write, create, and manipulate DESCRIPTION files. It is
    intended for packages that create or manipulate other packages."""

    cran = "desc"

    license("MIT")

    version("1.4.3", sha256="54468da73dd78fc9e7c565c41cfe3331802c2134b2e61a9ad197215317092f26")
    version("1.4.2", sha256="758acf14be478c09ba7e84ade3a7ce512becf35d44e5e6a997b932065f2a227c")
    version("1.4.1", sha256="8f9ebb51eccf925b2e76bc65ecf495e8f3882b8c0053023f396622f0402d6f54")
    version("1.4.0", sha256="8220e4c706449b8121b822e70b1414f391ef419aed574836a234c63b83e5d649")
    version("1.2.0", sha256="e66fb5d4fc7974bc558abcdc107a1f258c9177a29dcfcf9164bc6b33dd08dae8")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@1.4.1:")
    depends_on("r-cli", type=("build", "run"), when="@1.4.1:")
    depends_on("r-r6", type=("build", "run"))

    depends_on("r-rprojroot", type=("build", "run"), when="@:1.4.2")
    depends_on("r-assertthat", type=("build", "run"), when="@:1.2")
    depends_on("r-crayon", type=("build", "run"), when="@:1.4.0")
