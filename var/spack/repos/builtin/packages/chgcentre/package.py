# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Chgcentre(CMakePackage):
    """The chgcentre tool can be used
    to change the phase centre of a measurement set."""

    homepage = "https://sourceforge.net/p/wsclean/wiki/chgcentre/"
    url = "https://downloads.sourceforge.net/project/wsclean/chgcentre-1.6/chgcentre-1.6.tar.bz2"

    version("1.6", sha256="5b14f9f56b900072c42dab2a8217cd399fb1bb50aae20f9e3b6ff30ec5b12008")

    depends_on("cxx", type="build")  # generated

    depends_on("casacore")
    depends_on("gsl")

    # this patch is required to fix a programming error that is not acceptable by
    # latest compilers. In particular, the `std::min` function was given `int` and
    # `unsigned int` arguments. The `int` argument is explicitly casted to `unsigned int`.
    # This patch was created by the staff at the Pawsey Supercomputing Research Centre.
    patch("main.patch")
