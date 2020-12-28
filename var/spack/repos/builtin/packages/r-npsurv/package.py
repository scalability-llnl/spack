# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNpsurv(RPackage):
    """Contains functions for non-parametric survival analysis of exact and
    interval-censored observations."""

    homepage = "https://www.stat.auckland.ac.nz/~yongwang"
    url      = "https://cloud.r-project.org/src/contrib/npsurv_0.4-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/npsurv"

    version('0.4-0', sha256='404cf7135dc40a04e9b81224a543307057a8278e11109ba1fcaa28e87c6204f3')

    depends_on('r-lsei', type=('build', 'run'))
