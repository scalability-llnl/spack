# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGsodr(RPackage):
    """A Global Surface Summary of the Day (GSOD) Weather Data Client for R"""

    homepage = "https://docs.ropensci.org/GSODR/"
    url      = "https://cloud.r-project.org/src/contrib/GSODR_2.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/GSODR"

    version('2.1.1', sha256='dba732e5bd1e367b9d710e6b8924f0c02fa4546202f049124dba02bc2e3329f5')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-countrycode', type=('build', 'run'))
    depends_on('r-curl', type=('build', 'run'))
    depends_on('r-data-table@1.11.6:', type=('build', 'run'))
    depends_on('r-future-apply', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-r-utils', type=('build', 'run'))
