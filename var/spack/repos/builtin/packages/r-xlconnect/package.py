# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXlconnect(RPackage):
    """Provides comprehensive functionality to read, write and format Excel
    data."""

    homepage = "http://miraisolutions.wordpress.com/"
    url      = "https://cloud.r-project.org/src/contrib/XLConnect_0.2-11.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/XLConnect"

    version('0.2-15', sha256='26e1d8db65974719adbc25f1327c584003eb562dc1bb2121bffc2550cf3178b3')
    version('0.2-14', sha256='d1013ed26947572bad97d62a3d66346f74993cf96c6408d21d5b6ee567468819')
    version('0.2-12', sha256='500624f078fb27338aa91d8710daaf38633659a9b17f7cb713232a3d66f9f62c')
    version('0.2-11', sha256='17c5eddd00b933fd7a2ab9d942c813046d45f0af487f8d5b11011a004db69d0b')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-xlconnectjars@0.2-15', type=('build', 'run'))
    depends_on('r-rjava', type=('build', 'run'))
    depends_on('java@6:')
