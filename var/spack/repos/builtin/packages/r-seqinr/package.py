# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSeqinr(RPackage):
    """Exploratory data analysis and data visualization for biological
    sequence (DNA and protein) data. Includes also utilities for sequence
    data management under the ACNUC system."""

    homepage = "http://seqinr.r-forge.r-project.org"
    url      = "https://cloud.r-project.org/src/contrib/seqinr_3.3-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/seqinr"

    version('3.4-5', sha256='162a347495fd52cbb62e8187a4692e7c50b9fa62123c5ef98f2744c98a05fb9f')
    version('3.3-6', sha256='42a3ae01331db744d67cc9c5432ce9ae389bed465af826687b9c10216ac7a08d')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-ade4', type=('build', 'run'))
    depends_on('r-segmented', type=('build', 'run'))
    depends_on('zlib')
