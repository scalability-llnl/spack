# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCpp11(RPackage):
    """A C++11 Interface for R's C Interface.

    Provides a header only, C++11 interface to R's C interface. Compared to
    other approaches 'cpp11' strives to be safe against long jumps from the C
    API as well as C++ exceptions, conform to normal R function semantics and
    supports interaction with 'ALTREP' vectors."""

    cran = "cpp11"

    license("MIT")

    version("0.4.7", sha256="801d1266824c3972642bce2db2a5fd0528a65ec845c58eb5a886edf082264344")
    version("0.4.3", sha256="f1a60e4971a86dbbcf6a16bbd739b59bb66d9c45d93cfd8dedc2a87e302598f1")
    version("0.4.2", sha256="403ce0bf82358d237176053b0fb1e958cb6bfa4d0fb3555bf5801db6a6939b99")
    version("0.4.0", sha256="1768fd07dc30dfbbf8f3fb1a1183947cb7e1dfd909165c4d612a63c163a41e87")
    version("0.2.5", sha256="6fef9306c0c3043252c987e77c99ef679b2ea46dffafae318dbeb38ad21a2e20")

    depends_on("r@3.5.0:", when="@0.4.6:", type=("build", "run"))
