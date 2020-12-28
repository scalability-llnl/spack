# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPspline(RPackage):
    """Smoothing splines with penalties on order m derivatives."""

    homepage = "https://cloud.r-project.org/package=pspline"
    url      = "https://cloud.r-project.org/src/contrib/pspline_1.0-18.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pspline"

    version('1.0-18', sha256='f71cf293bd5462e510ac5ad16c4a96eda18891a0bfa6447dd881c65845e19ac7')

    depends_on('r@2.0.0:', type=('build', 'run'))
