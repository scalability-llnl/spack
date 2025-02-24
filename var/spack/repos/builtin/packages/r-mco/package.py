# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMco(RPackage):
    """Multiple Criteria Optimization Algorithms and Related Functions.

    A collection of function to solve multiple criteria optimization problems
    using genetic algorithms (NSGA-II). Also included is a collection of test
    functions."""

    cran = "mco"

    license("GPL-2.0-only")

    version("1.17", sha256="8288e99159a541855bd286baf586e61201e286dfd244080aef128871b1699ea2")
    version("1.15.6", sha256="17ebe279cb9c89b7cd8054ac50d3b657d2b10dadbc584b88da7e79c3a9680582")
    version("1.0-15.1", sha256="3c13ebc8c1f1bfa18f3f95b3998c57fde5259876e92456b6c6d4c59bef07c193")
    version("1.0-15", sha256="a25e3effbb6dcae735fdbd6c0bfc775e9fbbcc00dc00076b69c53fe250627055")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@1.17:")
