# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RChampdata(RPackage):
    """Packages for ChAMP package:

    Provides datasets needed for ChAMP including a test dataset and blood
    controls for CNA analysis."""

    bioc     = "ChAMPdata"

    version('2.22.0', commit='eeedd4c477fac79f00743da8ff7da064221c5f3d')

    depends_on('r@3.3:', type=('build', 'run'))
    depends_on('r-genomicranges@1.22.4:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.16.1:', type=('build', 'run'))
