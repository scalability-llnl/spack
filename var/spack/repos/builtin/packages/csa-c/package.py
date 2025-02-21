# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CsaC(AutotoolsPackage):
    """csa: Cubic Spline Approximation. csa is a C code for
    cubic spline approximation of 2D scattered data. It provides
    a C library and a command line utility csabathy."""

    homepage = "https://github.com/sakov/csa-c"
    git = "https://github.com/sakov/csa-c.git"

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    configure_directory = "csa"
