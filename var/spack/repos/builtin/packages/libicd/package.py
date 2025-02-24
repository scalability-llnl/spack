# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libicd(CMakePackage):
    """Image codec library."""

    homepage = "https://github.com/lucianpls/libicd"
    git = "https://github.com/lucianpls/libicd.git"

    license("Apache-2.0")

    version("main", branch="main")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.5:", type="build")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("lerc")
