# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class REnvstats(RPackage):
    """Package for Environmental Statistics, Including US EPA Guidance

    Graphical and statistical analyses of environmental data, with  focus on
    analyzing chemical concentrations and physical parameters, usually in  the
    context of mandated environmental monitoring.  Major environmental
    statistical methods found in the literature and regulatory guidance
    documents,  with extensive help that explains what these methods do, how to
    use them,  and where to find them in the literature.  Numerous built-in
    data sets from  regulatory guidance documents and environmental statistics
    literature.  Includes  scripts reproducing analyses presented in the book
    "EnvStats:  An R Package for  Environmental Statistics" (Millard, 2013,
    Springer, ISBN 978-1-4614-8455-4,
    <https://www.springer.com/book/9781461484554>)."""

    homepage = "https://cloud.r-project.org/package=EnvStats"
    url      = "https://cloud.r-project.org/src/contrib/EnvStats_2.3.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/EnvStats"

    version('2.4.0', sha256='49459e76412037b3d8021bd83ee93d140bc3e715a2a2282a347ef60061900514')
    version('2.3.1', sha256='d753d42b42ff28c1cd25c63916fb2aa9e325941672fb16f7dfd97e218416cf2a')
    version('2.3.0', sha256='51b7c982b4ffc6506579ec6933c817b780b8dade9f5e7754122e4132cb677a75')
    version('2.2.1', sha256='bbad7736272a404302190ccf1095abd8674d4366f3827a1c0a9540bcafe0523e')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-nortest', type=('build', 'run'))
