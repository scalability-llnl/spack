# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRsqlite(RPackage):
    """This package embeds the SQLite database engine in R and provides an
    interface compliant with the DBI package. The source for the SQLite engine
    (version 3.8.6) is included."""

    homepage = "https://cloud.r-project.org/package=RSQLite"
    url      = "https://cloud.r-project.org/src/contrib/RSQLite_2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RSQLite"

    version('2.1.2', sha256='66dad425d22b09651c510bf84b7fc36375ce537782f02585cf1c6856ae82d9c6')
    version('2.1.0', sha256='ad6081be2885be5921b1a44b1896e6a8568c8cff40789f43bfaac9f818767642')
    version('2.0', sha256='7f0fe629f34641c6af1e8a34412f3089ee2d184853843209d97ffe29430ceff6')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-dbi@1.0.0:', type=('build', 'run'))
    depends_on('r-bit64', type=('build', 'run'))
    depends_on('r-blob@1.2.0:', type=('build', 'run'))
    depends_on('r-memoise', type=('build', 'run'))
    depends_on('r-pkgconfig', type=('build', 'run'))
    depends_on('r-rcpp@0.12.7:', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'run'))
    depends_on('r-plogr@0.2.0:', type=('build', 'run'))
