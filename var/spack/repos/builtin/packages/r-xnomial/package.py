# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# See the Spack documentation for more information on packaging.

from spack.package import *


class RXnomial(RPackage):
    """Exact Goodness-of-Fit Test for Multinomial Data with Fixed
    Probabilities.

    Tests whether a set of counts fit a given expected ratio. For example, a
    genetic cross might be expected to produce four types in the relative
    frequencies of 9:3:3:1. To see whether a set of observed counts fits this
    expectation, one can examine all possible outcomes with xmulti() or a
    random sample of them with xmonte() and find the probability of an
    observation deviating from the expectation by at least as much as the
    observed. As a measure of deviation from the expected, one can use the
    log-likelihood ratio, the multinomial probability, or the classic
    chi-square statistic. A histogram of the test statistic can also be plotted
    and compared with the asymptotic curve."""

    cran = "XNomial"

    version("1.0.4", sha256="e6237f79d96f02bb30af1cf055ae9f70541abba34ce045a9d4359b5304189dd7")

    depends_on("c", type="build")  # generated

    depends_on("r@2.14:", type=("build", "run"))
