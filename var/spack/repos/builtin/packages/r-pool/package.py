# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPool(RPackage):
    """Object Pooling

    Enables the creation of object pools, which make it less computationally
    expensive to fetch a new object. Currently the only supported pooled
    objects are 'DBI' connections."""

    homepage = "https://github.com/rstudio/pool"
    cran     = "pool"

    version('0.1.6', sha256='cdbe5f6c7f757c01893dc9870df0fb8d300829da0e427f6c2559b01caa52d9e1')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-later@1.0.0:', type=('build', 'run'))
