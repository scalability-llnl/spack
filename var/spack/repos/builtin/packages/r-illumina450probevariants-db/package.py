# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIllumina450probevariantsDb(RPackage):
    """Annotation Package combining variant data from 1000 Genomes Project for
    Illumina HumanMethylation450 Bead Chip probes:

    Includes details on variants for each probe on the 450k bead chip for each
    of the four populations (Asian, American, African and European)."""

    bioc     = "Illumina450ProbeVariants.db"

    version('1.26.0', commit='fffe6033cc8d87354078c14de1e29976eaedd611')

    depends_on('r@3.0.1:', type=('build', 'run'))
