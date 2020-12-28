# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTweenr(RPackage):
    """tweenr: Interpolate Data for Smooth Animations"""

    homepage = "https://github.com/thomasp85/tweenr"
    url      = "https://cloud.r-project.org/src/contrib/tweenr_1.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tweenr"

    version('1.0.1', sha256='efd68162cd6d5a4f6d833dbf785a2bbce1cb7b9f90ba3fb060931a4bd705096b')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-farver', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-rcpp@0.12.3:', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
