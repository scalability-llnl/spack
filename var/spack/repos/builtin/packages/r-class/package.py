# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RClass(RPackage):
    """Various functions for classification, including k-nearest neighbour,
    Learning Vector Quantization and Self-Organizing Maps."""

    homepage = "http://www.stats.ox.ac.uk/pub/MASS4/"
    url      = "https://cloud.r-project.org/src/contrib/class_7.3-14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/class"

    version('7.3-15', sha256='f6bf33d610c726d58622b6cea78a808c7d6a317d02409d27c17741dfd1c730f4')
    version('7.3-14', sha256='18b876dbc18bebe6a00890eab7d04ef72b903ba0049d5ce50731406a82426b9c')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
