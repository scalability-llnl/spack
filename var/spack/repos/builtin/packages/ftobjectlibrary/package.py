# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ftobjectlibrary(CMakePackage):
    """FTObjectLibrary provides a collection of reference counted Fortran 2003
    classes to facilitate writing generic object oriented Fortran programs."""

    homepage = "https://github.com/trixi-framework/FTObjectLibrary"
    url = "https://github.com/trixi-framework/FTObjectLibrary"
    git = "https://github.com/trixi-framework/FTObjectLibrary.git"

    maintainers("schoonovernumerics")

    license("MIT")

    version("main", branch="main")

    depends_on("fortran", type="build")  # generated
