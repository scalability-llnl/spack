# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVfs(RPackage):
    """Vegetated Filter Strip and Erosion Model.

    Empirical models for runoff, erosion, and phosphorus loss across a
    vegetated filter strip, given slope, soils, climate, and vegetation (Gall
    et al., 2018) <doi:10.1007/s00477-017-1505-x>. It also includes functions
    for deriving climate parameters from measured daily weather data, and for
    simulating rainfall. Models implemented include MUSLE (Williams, 1975) and
    APLE (Vadas et al., 2009 <doi:10.2134/jeq2008.0337>)."""

    cran = "VFS"

    version("1.0.2", sha256="8ff7e7e13919ff21f10c7c693ef596a2c7b57c7ca37d79278e443ed122a21aad")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r-e1071", type=("build", "run"))
    depends_on("r-nleqslv@3.3.0:", type=("build", "run"))
