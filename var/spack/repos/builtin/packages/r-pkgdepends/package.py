# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPkgdepends(RPackage):
    """Package Dependency Resolution and Downloads.

    Find recursive dependencies of 'R' packages from various sources. Solve the
    dependencies to obtain a consistent set of packages to install. Download
    packages, and install them. It supports packages on 'CRAN', 'Bioconductor'
    and other 'CRAN-like' repositories, 'GitHub', package 'URLs', and local
    package trees and files. It caches metadata and package files via the
    'pkgcache' package, and performs all 'HTTP' requests, downloads, builds and
    installations in parallel. 'pkgdepends' is the workhorse of the 'pak'
    package."""

    cran = "pkgdepends"

    license("MIT")

    version("0.7.2", sha256="b17e22d01250916b06868317359239ca9273d7765b5ead9481b47cf0d96acd26")
    version("0.5.0", sha256="eadc98e335f9d2cc10b31cf7a5b55fe3308266fbd6f46d5dbd37b5d90bfcf1bc")
    version("0.3.2", sha256="61db529965f973847b4d1337c6556527a89953cad09d231a6e6ca2145a426a21")
    version("0.3.1", sha256="8e4263a1792871ee9629b0d6a8caeb53b77012db3b5be91b432f3553cd2a80be")
    version("0.2.0", sha256="59afdbe0e59663088ba4facac5cd011a0a05b0b9c540103fb8b9f0a673bf4d94")

    depends_on("r@3.4:", type=("build", "run"), when="@0.3.1:")
    depends_on("r@3.5:", type=("build", "run"), when="@0.7.0:")
    depends_on("r-callr@3.3.1:", type=("build", "run"))
    depends_on("r-cli@2.1.0:", type=("build", "run"))
    depends_on("r-cli@3.6.0:", type=("build", "run"), when="@0.5.0:")
    depends_on("r-curl", type=("build", "run"))
    depends_on("r-desc@1.2.0:", type=("build", "run"))
    depends_on("r-desc@1.4.3:", type=("build", "run"), when="@0.7.1:")
    depends_on("r-filelock@1.0.2:", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-lpsolve", type=("build", "run"))
    depends_on("r-pkgbuild@1.0.2:", type=("build", "run"))
    depends_on("r-pkgcache@1.3.0:", type=("build", "run"))
    depends_on("r-pkgcache@2.0.0:", type=("build", "run"), when="@0.3.1:")
    depends_on("r-pkgcache@2.1.0:", type=("build", "run"), when="@0.5.0:")
    depends_on("r-pkgcache@2.2.0:", type=("build", "run"), when="@0.6.0:")
    depends_on("r-processx@3.4.2:", type=("build", "run"))
    depends_on("r-ps", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-zip@2.1.0:", type=("build", "run"))
    depends_on("r-zip@2.3.0:", type=("build", "run"), when="@0.5.0:")

    depends_on("r-glue", type=("build", "run"), when="@:0.7.0")
    depends_on("r-prettyunits@1.1.1:", type=("build", "run"), when="@:0.7.0")
    depends_on("r-rprojroot", type=("build", "run"), when="@:0.7.0")
    depends_on("r-withr@2.1.1:", type=("build", "run"), when="@:0.5.0")
    depends_on("r-rematch2", type=("build", "run"), when="@:0.2.0")
    depends_on("r-tibble", type=("build", "run"), when="@:0.2.0")
    depends_on("r-crayon", type=("build", "run"), when="@:0.3.2")
