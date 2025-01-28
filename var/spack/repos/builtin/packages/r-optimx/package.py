# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ROptimx(RPackage):
    """Expanded Replacement and Extension of the 'optim' Function.

    Provides a replacement and extension of the optim() function to call to
    several function minimization codes in R in a single statement. These
    methods handle smooth, possibly box constrained functions of several or
    many parameters. Note that function 'optimr()' was prepared to simplify the
    incorporation of minimization codes going forward. Also implements some
    utility codes and some extra solvers, including safeguarded Newton methods.
    Many methods previously separate are now included here. This is the version
    for CRAN."""

    cran = "optimx"

    license("GPL-2.0-only")

    version(
        "2023-10.21", sha256="0d732d5604c26af59cfb95b80ed4e226c9c10422e2d82a6cc06b92f9ba6a44b5"
    )
    version("2022-4.30", sha256="ebe9887a22296cf4b2db07981aaa1f898bf7c17fb61a4b398c228d4077d0b410")
    version(
        "2021-10.12", sha256="39384c856b5efa3992cd230548b60eff936d428111ad6ad5b8fb98a3bcbb7943"
    )
    version("2020-4.2", sha256="6381c25c322287fc98ab1b2965d3f68c9a92c587c76aca1d33fd6428b2167101")

    depends_on("r-nloptr", type=("build", "run"), when="@2023-10.21:")
    depends_on("r-numderiv", type=("build", "run"))
    depends_on("r-pracma", type=("build", "run"), when="@2023-10.21:")
