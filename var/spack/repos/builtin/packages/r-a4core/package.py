# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RA4core(RPackage):
    """Automated Affymetrix Array Analysis Core Package.

    Utility functions for the Automated Affymetrix Array Analysis set of
    packages."""

    bioc = "a4Core"

    version("1.48.0", commit="3dd09f0a662745fcfd3fee7048301f3524e8ac5c")
    version("1.46.0", commit="8999fe146be6d04ae36c725d2b6324a6ce8ceb83")
    version("1.44.0", commit="61a7f3a51a41af615bfd4c22984e4c4a82874e8c")
    version("1.42.0", commit="6985950b72c2a0f20ec44fe2067d8864e004bfaa")
    version("1.38.0", commit="a027dcd3486c64950815ec7c7271f1f65ba3d8a1")
    version("1.32.0", commit="2916a29723bdd514d5d987f89725d141d1d2dfce")
    version("1.30.0", commit="e392b1b4339a34f93d5d9bc520a1a9385ea63141")
    version("1.28.0", commit="39b6ee29bc2f2fdc5733438c14dc02f8abc6460b")
    version("1.26.0", commit="e7be935f20b486165a2b27dbbf9e99ba07151bcd")
    version("1.24.0", commit="c871faa3e1ab6be38a9ea3018816cf31b58b0ed3")

    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-glmnet", type=("build", "run"))
