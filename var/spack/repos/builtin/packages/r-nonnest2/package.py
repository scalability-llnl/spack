# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNonnest2(RPackage):
    """Tests of Non-Nested Models:

    Testing non-nested models via theory supplied by Vuong (1989)
    <doi:10.2307/1912557>. Includes tests of model distinguishability and of
    model fit that can be applied to both nested and non-nested models. Also
    includes functionality to obtain confidence intervals associated with AIC
    and BIC. This material is partially based on work supported by the National
    Science Foundation under Grant Number SES-1061334."""

    cran     = "nonnest2"

    version('0.5-5', sha256='027f510e322122fc75c936251a95ddd392f96047ac86e0fae6cf8f883ac7aab5')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-compquadform', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-lavaan@0.6-6:', type=('build', 'run'))
    depends_on('r-sandwich', type=('build', 'run'))
