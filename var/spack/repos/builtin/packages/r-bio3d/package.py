# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBio3d(RPackage):
    """bio3d: Biological Structure Analysis"""

    homepage = "http://thegrantlab.org/bio3d/"
    url      = "https://cloud.r-project.org/src/contrib/bio3d_2.3-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/bio3d"

    version('2.3-4', sha256='f9b39ab242cbedafcd98c1732cb1f5c0dd9ef66e28be39695e3420dd93e2bafe')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
