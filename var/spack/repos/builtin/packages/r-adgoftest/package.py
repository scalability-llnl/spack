# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAdgoftest(RPackage):
    """Anderson-Darling GoF test.

    Anderson-Darling GoF test with p-value calculation based on Marsaglia's
    2004 paper 'Evaluating the Anderson-Darling Distribution'."""

    cran = "ADGofTest"

    version("0.3", sha256="9cd9313954f6ecd82480d373f6c5371ca84ab33e3f5c39d972d35cfcf1096846")
