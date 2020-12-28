# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFields(RPackage):
    """fields: Tools for Spatial Data"""

    homepage = "https://github.com/NCAR/Fields"
    url      = "https://cloud.r-project.org/src/contrib/fields_9.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fields"

    version('9.9', sha256='262f03c630773b580c7162ab2a031c894ca489fd83989fd8a2f67573306e78e1')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-maps', type=('build', 'run'))
    depends_on('r-spam', type=('build', 'run'))
