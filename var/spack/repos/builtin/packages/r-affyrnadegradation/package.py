# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffyrnadegradation(RPackage):
    """Analyze and correct probe positional bias in microarray data due to RNA
       degradation.

       The package helps with the assessment and correction of RNA degradation
       effects in Affymetrix 3' expression arrays. The parameter d gives a
       robust and accurate measure of RNA integrity. The correction removes the
       probe positional bias, and thus improves comparability of samples that
       are affected by RNA degradation."""

    homepage = "https://bioconductor.org/packages/AffyRNADegradation"
    git      = "https://git.bioconductor.org/packages/AffyRNADegradation.git"

    version('1.30.0', commit='620c464fb09248e1c7a122828eab59a4fb778cc1')
    version('1.28.0', commit='aff91d78fa9e76edaa3ef6a9a43b98b86cc44c24')
    version('1.26.0', commit='6ab03ad624701464280bf7dfe345d200e846298a')
    version('1.24.0', commit='1f85f3da4720cef94623828713eb84d8accbcf8a')
    version('1.22.0', commit='0fa78f8286494711a239ded0ba587b0de47c15d3')

    depends_on('r@2.9.0:', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
