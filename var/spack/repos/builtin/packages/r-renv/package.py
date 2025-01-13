# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRenv(RPackage):
    """Project Environments for R packages.

    A dependency management toolkit for R. Using 'renv', you can create and
    manage project-local R libraries, save the state of these libraries to a
    'lockfile', and later restore your library as required. Together, these
    tools can help make your projects more isolated, portable, and
    reproducible."""

    cran = "renv"

    license("MIT")

    version("1.0.7", sha256="7b60b58a23743803ab167f82f78663e86f778947b2bda07afa12689338794507")
    version("0.17.3", sha256="1c4f28cd233e1f539a2a091f1d118de83eb8aea5d5780dbdfb6bb8dcc6e4f5f0")
    version("0.16.0", sha256="f3a13e6b71e9be460db73bd9e11a3cb8a1d9bc05c6b77423957cbc2a7f8ba016")
    version("0.15.5", sha256="b4f1a9a7daa82f0c3123ebd4eeba06e98d5485215518e5292b25bc56741d582e")
    version("0.15.2", sha256="d07effd329f6d653fec9cb517bc8adf3cd6b711758e439055b6d2f06c88765db")
    version("0.15.1", sha256="36e8c8df4af50f2341053aa567798dfca6852ade10fa70f9dc146fe9f96f9b5b")
    version("0.13.2", sha256="41f208ed957e27c50cbd8b0fff77a434bad963707df85e462419e2edb6719a4a")
