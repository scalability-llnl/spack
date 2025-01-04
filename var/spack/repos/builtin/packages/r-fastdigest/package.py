# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFastdigest(RPackage):
    """Fast, Low Memory-Footprint Digests of R Objects.

    Provides an R interface to Bob Jenkin's streaming, non-cryptographic
    'SpookyHash' hash algorithm for use in digest-based comparisons of R
    objects. 'fastdigest' plugs directly into R's internal serialization
    machinery, allowing digests of all R objects the serialize() function
    supports, including reference-style objects via custom hooks. Speed is high
    and scales linearly by object size; memory usage is constant and
    negligible."""

    cran = "fastdigest"

    maintainers("dorton21")

    license("Artistic-2.0")

    version("0.6-4", sha256="b2b6a550d90446bed911c9ad7642efd2a869257ecc5b9eb57e66b2cd4ef109a0")
    version("0.6-3", sha256="62a04aa39f751cf9bb7ff43cadb3c1a8d2270d7f3e8550a2d6ca9e1d8ca09a09")
