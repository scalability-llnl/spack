# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRstantools(RPackage):
    """Tools for Developing R Packages Interfacing with 'Stan'.

    Provides various tools for developers of R packages interfacing with 'Stan'
    <https://mc-stan.org>, including functions to set up the required  package
    structure, S3 generics and default methods to unify function naming  across
    'Stan'-based R packages, and vignettes with recommendations for
    developers."""

    cran = "rstantools"

    license("GPL-3.0-or-later")

    version("2.4.0", sha256="bff72ca2f0352c6c5d2868823e286fdb73a6ead74508a4124cbcb222c83b4faa")
    version("2.3.1", sha256="82d4f2e884ffc894463bd37765606d5a9bef2ee631758840ec58636acdca6975")
    version("2.2.0", sha256="cb810baeb90c67668361b666c6862df9917aff6aaec63d2c3a485f28407c4eb7")
    version("2.1.1", sha256="c95b15de8ec577eeb24bb5206e7b685d882f88b5e6902efda924b7217f463d2d")
    version("1.5.1", sha256="5cab16c132c12e84bd08e18cd6ef25ba39d67a04ce61015fc4490659c7cfb485")

    depends_on("r+X", type=("build", "run"))
    depends_on("r-desc", type=("build", "run"), when="@2.1.1:")
    depends_on("r-rcpp@0.12.16:", type=("build", "run"), when="@2.1.1:")
    depends_on("r-rcppparallel@5.0.1:", type=("build", "run"), when="@2.1.1:")
    depends_on("pandoc", type="build")
