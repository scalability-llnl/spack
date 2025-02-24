# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMicrobenchmark(RPackage):
    """Accurate Timing Functions.

    Provides infrastructure to accurately measure and compare the execution
    time of R expressions."""

    cran = "microbenchmark"

    license("BSD-2-Clause")

    version("1.4.10", sha256="04cc41be72708dce8d31ff1cb105d88cc9f167250ea00fe9a165c99204b9b481")
    version("1.4.9", sha256="443d2caf370ef33e4ac2773176ad9eb86f8790f43b430968ef9647699dbbffd2")
    version("1.4-7", sha256="268f13c6323dd28cc2dff7e991bb78b814a8873b4a73f4a3645f40423da984f6")
