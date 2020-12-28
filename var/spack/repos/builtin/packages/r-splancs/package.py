# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSplancs(RPackage):
    """Spatial and Space-Time Point Pattern Analysis"""

    homepage = "https://cloud.r-project.org/package=splancs"
    url      = "https://cloud.r-project.org/src/contrib/splancs_2.01-40.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/splancs"

    version('2.01-40', sha256='79744381ebc4a361740a36dca3c9fca9ae015cfe0bd585b7856a664a3da74363')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-sp@0.9:', type=('build', 'run'))
