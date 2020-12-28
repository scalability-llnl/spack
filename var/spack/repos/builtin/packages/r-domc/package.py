# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDomc(RPackage):
    """Provides a parallel backend for the %dopar% function using
    the multicore functionality of the parallel package."""

    homepage = "https://cloud.r-project.org/package=doMC"
    url      = "https://cloud.r-project.org/src/contrib/doMC_1.3.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/doMC"

    version('1.3.6', sha256='2977fc9e2dc54d85d45b4a36cd286dff72834fbc73f38b6ee45a6eb8557fc9b2')
    version('1.3.4', sha256='76a1092fca59b441e6f89eb7e2fb3a12de807f736a217949c80339f20c958778')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-foreach@1.2.0:', type=('build', 'run'))
    depends_on('r-iterators@1.0.0:', type=('build', 'run'))
