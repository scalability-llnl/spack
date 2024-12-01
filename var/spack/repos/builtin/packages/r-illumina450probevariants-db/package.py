# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIllumina450probevariantsDb(RPackage):
    """Annotation Package combining variant data from 1000 Genomes Project for
    Illumina HumanMethylation450 Bead Chip probes.

    Includes details on variants for each probe on the 450k bead chip for each
    of the four populations (Asian, American, African and European)."""

    bioc = "Illumina450ProbeVariants.db"

    version("1.36.0", commit="aaa4254cebb352730779677cef7a7c99c1447e7a")
    version("1.34.0", commit="6c0f0b4d2bcf13da852b2f132a8ce1229fa5269e")
    version("1.32.0", commit="a15602253e675a104303627957653a08876d8d7c")
    version("1.30.0", commit="ba1296b4aafc287dea61f5f37c6c99fd553e52a2")
    version("1.26.0", commit="fffe6033cc8d87354078c14de1e29976eaedd611")

    depends_on("r@3.0.1:", type=("build", "run"))
