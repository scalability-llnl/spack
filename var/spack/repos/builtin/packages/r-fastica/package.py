# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFastica(RPackage):
    """FastICA Algorithms to Perform ICA and Projection Pursuit:

    Implementation of FastICA algorithm to perform Independent Component
    Analysis (ICA) and Projection Pursuit."""

    cran     = "fastICA"

    version('1.2-2', sha256='32223593374102bf54c8fdca7b57231e4f4d0dd0be02d9f3500ad41b1996f1fe')

    depends_on('r@3.0.0:', type=('build', 'run'))
