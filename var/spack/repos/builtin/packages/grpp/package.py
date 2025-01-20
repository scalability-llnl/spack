# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import autotools, cmake
from spack.package import *


class Grpp(CMakePackage):
    """ GRPP: A library for the evaluation of molecular integrals
       of the generalized relativistic pseudopotential operator
       (GRPP) over Gaussian functions."""

    #
    # The package has no official version and did not see a lot
    # of development activities in 2024. It is used in cp2k and
    # is needed when cp2k is build with trexio support
    #

    homepage = "https://github.com/aoleynichenko/libgrpp"
    git = "https://github.com/aoleynichenko/libgrpp.git"

    # notify when the package is updated.
    maintainers("mtaillefumier")

    license("BSD-3-Clause")

    build_system("cmake")

    version("master", branch="main")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    depends_on("cmake", type="build")

    patch("grpp-cmake.patch")
