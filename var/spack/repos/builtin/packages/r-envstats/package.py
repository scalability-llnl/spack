# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REnvstats(RPackage):
    """Graphical and statistical analyses of environmental data, with focus
       on analyzing chemical concentrations and physical parameters, usually
       in the context of mandated environmental monitoring.
    """

    homepage = "https://cloud.r-project.org/package=EnvStats"
    url      = "https://cloud.r-project.org/src/contrib/EnvStats_2.3.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/EnvStats"

    version('2.3.1', sha256='d753d42b42ff28c1cd25c63916fb2aa9e325941672fb16f7dfd97e218416cf2a')
    version('2.3.0', sha256='51b7c982b4ffc6506579ec6933c817b780b8dade9f5e7754122e4132cb677a75')
    version('2.2.1', sha256='bbad7736272a404302190ccf1095abd8674d4366f3827a1c0a9540bcafe0523e')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-nortest', type=('build', 'run'))
