# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLater(RPackage):
    """Utilities for Scheduling Functions to Execute Later with Event Loops.

    Executes arbitrary R or C functions some time after the current time, after
    the R execution stack has emptied."""

    cran = "later"

    license("MIT")

    version("1.3.2", sha256="52f5073d33cd0d3c12e56526c9c53c323ebafcc79b22cc6e51fb0c41ee2b561e")
    version("1.3.0", sha256="08f50882ca3cfd2bb68c83f1fcfbc8f696f5cfb5a42c1448c051540693789829")
    version("1.1.0.1", sha256="71baa7beae774a35a117e01d7b95698511c3cdc5eea36e29732ff1fe8f1436cd")
    version("0.8.0", sha256="6b2a28b43c619b2c7890840c62145cd3a34a7ed65b31207fdedde52efb00e521")

    depends_on("r-rcpp@0.12.9:", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))

    depends_on("r-bh", type=("build", "run"), when="@:1.1.0.1")
