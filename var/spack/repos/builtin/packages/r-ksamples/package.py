# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RKsamples(RPackage):
    """K-Sample Rank Tests and their Combinations.

    Compares k samples using the Anderson-Darling test, Kruskal-Wallis type
    tests with different rank score criteria, Steel's multiple comparison test,
    and the Jonckheere-Terpstra (JT) test. It computes asymptotic, simulated or
    (limited) exact P-values, all valid under randomization, with or without
    ties, or conditionally under random sampling from populations, given the
    observed tie pattern. Except for Steel's test and the JT test it also
    combines these tests across several blocks of samples. Also analyzed are 2
    x t contingency tables and their blocked combinations using the
    Kruskal-Wallis criterion. Steel's test is inverted to provide simultaneous
    confidence bounds for shift parameters. A plotting function compares tail
    probabilities obtained under asymptotic approximation with those obtained
    via simulation or exact calculations."""

    cran = "kSamples"

    version("1.2-10", sha256="2d66cc0511fb1be3190c5a285dcd93d02419468ee1ff5ae6d0838f16df2b578d")
    version("1.2-9", sha256="ba3ec4af3dfcf7cf12f0b784ef67bfea565e16985647ead904629886cc1542ff")

    depends_on("r-suppdists", type=("build", "run"))
