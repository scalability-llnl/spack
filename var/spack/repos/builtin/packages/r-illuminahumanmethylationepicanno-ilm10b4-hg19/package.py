# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIlluminahumanmethylationepicannoIlm10b4Hg19(RPackage):
    """Annotation for Illumina's EPIC methylation arrays"""

    homepage = "https://bitbucket.com/kasperdanielhansen/Illumina_EPIC"
    url      = "https://bioconductor.org/packages/release/data/annotation/src/contrib/IlluminaHumanMethylationEPICanno.ilm10b4.hg19_0.6.0.tar.gz"
    bioc     = "IlluminaHumanMethylationEPICanno.ilm10b4.hg19"

    version('0.6.0', sha256='2c8128126b63e7fa805a5f3b02449367dca9c3be3eb5f6300acc718826590719')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-minfi@1.19.15:', type=('build', 'run'))
