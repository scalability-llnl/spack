# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBigalgebra(RPackage):
    """This package provides arithmetic functions for R matrix
       and big.matrix objects."""

    homepage = "https://r-forge.r-project.org/R/?group_id=556"
    url      = "https://cloud.r-project.org/src/contrib/Archive/bigalgebra/bigalgebra_0.8.4.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/bigalgebra"

    version('0.8.4.2', sha256='29962468cbfa6416f8628563d5ed8c9f76089190311ff1c618f099ee8d9eea75')

    depends_on('r-bigmemory@4.0.0:', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'run'))
