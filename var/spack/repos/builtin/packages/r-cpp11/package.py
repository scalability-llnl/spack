# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RCpp11(RPackage):
    """cpp11: A C++11 Interface for R's C Interface

    Provides a header only, C++11 interface to R's C interface. Compared to
    other approaches 'cpp11' strives to be safe against long jumps from the C
    API as well as C++ exceptions, conform to normal R function semantics and
    supports interaction with 'ALTREP' vectors."""

    homepage = "https://github.com/r-lib/cpp11"
    url      = "https://cloud.r-project.org/src/contrib/cpp11_0.2.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/cpp11"

    version('0.2.5', sha256='6fef9306c0c3043252c987e77c99ef679b2ea46dffafae318dbeb38ad21a2e20')
