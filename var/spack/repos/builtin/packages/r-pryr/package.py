# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RPryr(RPackage):
    """Useful tools to pry back the covers of R and understand the language
    at a deeper level."""

    homepage = "https://github.com/hadley/pryr"
    url      = "https://cloud.r-project.org/src/contrib/pryr_0.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pryr"

    version('0.1.4', sha256='d39834316504c49ecd4936cbbcaf3ee3dae6ded287af42475bf38c9e682f721b')
    version('0.1.3', sha256='6acd88341dde4fe247a5cafd3949b281dc6742b7d60f68b57c1feb84b96739ac')
    version('0.1.2', sha256='65c2b7c9f96e2aa683ac9cdab3c215fd3039ecd66a2ba7002a8e77881428c3c6')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-codetools', type=('build', 'run'))
