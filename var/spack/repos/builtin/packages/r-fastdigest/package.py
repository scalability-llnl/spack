# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFastdigest(RPackage):
    """Fast, Low Memory-Footprint Digests of R Objects

    Provides an R interface to Bob Jenkin's streaming, non-cryptographic
    'SpookyHash' hash algorithm for use in digest-based comparisons of R
    objects. 'fastdigest' plugs directly into R's internal serialization
    machinery, allowing digests of all R objects the serialize() function
    supports, including reference-style objects via custom hooks. Speed is
    high and scales linearly by object size;
    memory usage is constant and negligible."""

    homepage = "https://cloud.r-project.org/web/packages/fastdigest/index.html"
    url      = "https://cloud.r-project.org/src/contrib/fastdigest_0.6-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fastdigest"

    maintainers = ['dorton21']

    version('0.6-3', sha256='62a04aa39f751cf9bb7ff43cadb3c1a8d2270d7f3e8550a2d6ca9e1d8ca09a09')
