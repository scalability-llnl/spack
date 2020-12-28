# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRCache(RPackage):
    """Memoization can be used to speed up repetitive and computational
    expensive function calls. The first time a function that implements
    memoization is called the results are stored in a cache memory. The next
    time the function is called with the same set of parameters, the results
    are momentarily retrieved from the cache avoiding repeating the
    calculations. With this package, any R object can be cached in a key-value
    storage where the key can be an arbitrary set of R objects. The cache
    memory is persistent (on the file system)."""

    homepage = "https://github.com/HenrikBengtsson/R.cache"
    url      = "https://cloud.r-project.org/src/contrib/R.cache_0.14.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/R.cache"

    version('0.14.0', sha256='18af4e372440b9f28b4b71346c8ed9de220232f9903730ccee2bfb3c612c16d9')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-r-methodss3@1.7.1:', type=('build', 'run'))
    depends_on('r-r-oo@1.23.0:', type=('build', 'run'))
    depends_on('r-r-utils@2.8.0:', type=('build', 'run'))
    depends_on('r-digest@0.6.13:', type=('build', 'run'))
