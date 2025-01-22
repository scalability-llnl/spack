# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Grpp(CMakePackage):
    """GRPP: A library for the evaluation of molecular integrals
    of the generalized relativistic pseudopotential operator
    (GRPP) over Gaussian functions."""

    #
    # The package has no official version and did not see a lot
    # of development activities in 2024. It is used in cp2k and
    # is needed when cp2k is build with trexio support
    #

    homepage = "https://github.com/aoleynichenko/libgrpp"
    git = "https://github.com/aoleynichenko/libgrpp.git"

    maintainers("mtaillefumier")

    license("BSD-3-Clause")

    build_system("cmake")

    version("main", branch="main")
    version(
        "2023.12.25", commit="64d157f1dc95815096b1fd437a5851abeb3425929cf7b2092bf8262db9c5e33d"
    )

    depends_on("c", type="build")
    depends_on("fortran", type="build")
    depends_on("cmake", type="build")

    patch("grpp-cmake.patch")
