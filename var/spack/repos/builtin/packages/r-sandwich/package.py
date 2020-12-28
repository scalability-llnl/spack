# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSandwich(RPackage):
    """Model-robust standard error estimators for cross-sectional, time series,
    and longitudinal data."""

    homepage = "https://cloud.r-project.org/package=sandwich"
    url      = "https://cloud.r-project.org/src/contrib/sandwich_2.3-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/sandwich"

    version('2.5-1', sha256='dbef6f4d12b83e166f9a2508b7c732b04493641685d6758d29f3609e564166d6')
    version('2.5-0', sha256='6cc144af20739eb23e5539010d3833d7c7fc53cbca2addb583ab933167c11399')
    version('2.3-4', sha256='2052f7e3d19a05c372f422c5480f1058a4107e420cd038a9bd7240c4f0746d4d')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
