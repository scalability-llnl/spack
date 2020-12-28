# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNcbit(RPackage):
    """Making NCBI taxonomic data locally available and searchable as an R
       object."""

    homepage = "https://cloud.r-project.org/package=ncbit"
    url      = "https://cloud.r-project.org/src/contrib/ncbit_2013.03.29.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ncbit"

    version('2013.03.29', sha256='4480271f14953615c8ddc2e0666866bb1d0964398ba0fab6cc29046436820738')

    depends_on('r@2.10:', type=('build', 'run'))
