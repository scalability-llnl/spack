# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RJade(RPackage):
    """Blind Source Separation Methods Based on Joint Diagonalization and Some
    BSS Performance Criteria.

    Cardoso's JADE algorithm as well as his functions for joint diagonalization
    are ported to R. Also several other blind source separation (BSS) methods,
    like AMUSE and SOBI, and some criteria for performance evaluation of BSS
    algorithms, are given. The package is described in Miettinen, Nordhausen
    and Taskinen (2017) <doi:10.18637/jss.v076.i02>."""

    cran = "JADE"

    version("2.0-4", sha256="d4b3d65a33cae454d3ab13343bceabfb3f6b8004ac64ae7bd86dee92a1cd2055")
    version("2.0-3", sha256="56d68a993fa16fc6dec758c843960eee840814c4ca2271e97681a9d2b9e242ba")

    depends_on("r-clue", type=("build", "run"))
