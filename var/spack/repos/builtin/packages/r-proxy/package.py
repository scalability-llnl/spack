# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProxy(RPackage):
    """Provides an extensible framework for the efficient calculation of
       auto- and cross-proximities, along with implementations of the most
       popular ones."""

    homepage = "https://cloud.r-project.org/package=proxy"
    url      = "https://cloud.r-project.org/src/contrib/proxy_0.4-19.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/proxy"

    version('0.4-23', sha256='9dd4eb0978f40e4fcb55c8a8a26266d32eff9c63ac9dfe70cf1f664ca9c3669d')
    version('0.4-19', sha256='6b27e275018366e6024382704da9a9757c8878535dbcd7d450824b70e2e34d51')

    depends_on('r@3.3.2:', when='@:0.4-20', type=('build', 'run'))
    depends_on('r@3.4.0:', when='@0.4-21:', type=('build', 'run'))
