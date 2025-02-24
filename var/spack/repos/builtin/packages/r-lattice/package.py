# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLattice(RPackage):
    """Trellis Graphics for R.

    A powerful and elegant high-level data visualization system inspired by
    Trellis graphics, with an emphasis on multivariate data. Lattice is
    sufficient for typical graphics needs, and is also flexible enough to
    handle most nonstandard requirements. See ?Lattice for an introduction."""

    cran = "lattice"

    license("GPL-2.0-or-later")

    version("0.22-6", sha256="4b377211e472ece7872b9d6759f9b9c660b09594500462eb6146312a1d4d00f7")
    version("0.21-8", sha256="8ad3d6974262e6cab6cc8fec38aa279b5b2f2524adf6f3eab56f68302b60c329")
    version("0.20-45", sha256="22388d92bdb7d3959da84d7308d9026dd8226ef07580783729e8ad2f7d7507ad")
    version("0.20-44", sha256="57b908e3c7ada08a38ad857ee44f44fdf9cfa59d5d9500bda2ccc9c7e96cdb9b")
    version("0.20-41", sha256="54ca557f0cb33df60eb10b883c2ed2847e061ddd57ed9b5dd7695149609d57b5")
    version("0.20-38", sha256="fdeb5e3e50dbbd9d3c5e2fa3eef865132b3eef30fbe53a10c24c7b7dfe5c0a2d")
    version("0.20-35", sha256="0829ab0f4dec55aac6a73bc3411af68441ddb1b5b078d680a7c2643abeaa965d")
    version("0.20-34", sha256="4a1a1cafa9c6660fb9a433b3a51898b8ec8e83abf143c80f99e3e4cf92812518")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@0.21-8:")
