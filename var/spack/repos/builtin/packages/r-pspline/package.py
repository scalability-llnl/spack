# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPspline(RPackage):
    """Penalized Smoothing Splines.

    Smoothing splines with penalties on order m derivatives."""

    cran = "pspline"

    version('1.0-18', sha256='f71cf293bd5462e510ac5ad16c4a96eda18891a0bfa6447dd881c65845e19ac7')

    depends_on('r@2.0.0:', type=('build', 'run'))
