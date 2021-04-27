# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RBio3d(RPackage):
    """Biological Structure Analysis

    Utilities to process, organize and explore protein structure, sequence and
    dynamics data. Features include the ability to read and write structure,
    sequence and dynamic trajectory data, perform sequence and structure
    database searches, data summaries, atom selection, alignment,
    superposition, rigid core identification, clustering, torsion analysis,
    distance matrix analysis, structure and sequence conservation analysis,
    normal mode analysis, principal component analysis of heterogeneous
    structure data, and correlation network analysis from normal mode and
    molecular dynamics data. In addition, various utility functions are
    provided to enable the statistical and graphical power of the R environment
    to work with biological sequence and structural data. Please refer to the
    URLs below for more information."""

    homepage = "http://thegrantlab.org/bio3d/"
    url      = "https://cloud.r-project.org/src/contrib/bio3d_2.3-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/bio3d"

    version('2.4-1', sha256='679fbd87fe9fb82a65427d281d3b68906509e411270cd87d2deb95d404333c1f')
    version('2.3-4', sha256='f9b39ab242cbedafcd98c1732cb1f5c0dd9ef66e28be39695e3420dd93e2bafe')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
