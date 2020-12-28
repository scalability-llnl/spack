# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDynamictreecut(RPackage):
    """dynamicTreeCut: Methods for Detection of Clusters in Hierarchical
       Clustering Dendrograms"""

    homepage = "https://cloud.r-project.org/package=dynamicTreeCut"
    url      = "https://cloud.r-project.org/src/contrib/dynamicTreeCut_1.63-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/dynamicTreeCut/"

    version('1.63-1', sha256='831307f64eddd68dcf01bbe2963be99e5cde65a636a13ce9de229777285e4db9')

    depends_on('r@2.3.0:', type=('build', 'run'))
