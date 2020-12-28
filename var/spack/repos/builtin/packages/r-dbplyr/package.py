# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDbplyr(RPackage):
    """A 'dplyr' back end for databases that allows you to work with remote
       database tables as if they are in-memory data frames. Basic features
       works with any database that has a 'DBI' back end; more advanced
       features require 'SQL' translation to be provided by the package
       author."""

    homepage = "https://github.com/tidyverse/dbplyr"
    url      = "https://cloud.r-project.org/src/contrib/dbplyr_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/dbplyr"

    version('1.4.2', sha256='b783f0da2c09a1e63f41168b02c0715b08820f02a351f7ab0aaa688432754de0')
    version('1.4.1', sha256='cfe829f56acdc785c5af21bf3927cf08327504d78c4ae1477c405c81b131da95')
    version('1.2.2', sha256='9d410bb0055fffe10f1f8da55a5b24d98322c7b571d74df61427d5888332bc48')
    version('1.2.1', sha256='b348e7a02623f037632c85fb11be16c40c01755ae6ca02c8c189cdc192a699db')
    version('1.2.0', sha256='02a5fa8dcf8a81c061fdaefa74f17896bee913720418b44dbd226a0d6b30799d')
    version('1.1.0', sha256='7b1e456a2d1056fa6284582cd82d2df66d06b3eea92e9995f5a91a45f246f69d')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-assertthat@0.2.0:', type=('build', 'run'))
    depends_on('r-dbi@1.0.0:', type=('build', 'run'))
    depends_on('r-dplyr@0.8.0:', type=('build', 'run'))
    depends_on('r-glue@1.2.0:', type=('build', 'run'))
    depends_on('r-purrr@0.2.5:', type=('build', 'run'))
    depends_on('r-r6@2.2.2:', type=('build', 'run'))
    depends_on('r-rlang@0.2.0:', type=('build', 'run'))
    depends_on('r-tibble@1.4.2:', type=('build', 'run'))
    depends_on('r-tidyselect@0.2.4:', type=('build', 'run'))
