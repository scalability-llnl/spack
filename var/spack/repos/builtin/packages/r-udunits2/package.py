# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUdunits2(RPackage):
    """Provides simple bindings to Unidata's udunits library."""

    homepage = "https://github.com/pacificclimate/Rudunits2"
    url      = "https://cloud.r-project.org/src/contrib/udunits2_0.13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/udunits2"

    version('0.13', sha256='d155d3c07f6202b65dec4075ffd1e1c3f4f35f5fdece8cfb319d39256a3e5b79')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('udunits')
