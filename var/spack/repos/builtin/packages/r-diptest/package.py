# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDiptest(RPackage):
    """Hartigan's Dip Test Statistic for Unimodality - Corrected.

    Compute Hartigan's dip test statistic for unimodality /; multimodality and
    provide a test with simulation based p-values,  where; the original public
    code has been corrected."""

    cran = "diptest"

    license("GPL-2.0-or-later")

    version("0.77-1", sha256="224eae00f483ce0fb131719065667227417cc98ad2beda55bfd5efe2bb612813")
    version("0.76-0", sha256="508a5ebb161519cd0fcd156dc047b51becb216d545d62c6522496463f94ec280")
    version("0.75-7", sha256="462900100ca598ef21dbe566bf1ab2ce7c49cdeab6b7a600a50489b05f61b61b")
