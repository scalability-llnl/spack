# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class REcp(RPackage):
    """Non-Parametric Multiple Change-Point Analysis of MultivariateData

    Implements various procedures for finding multiple change-points from
    Matteson D. et al (2013) <doi:10.1080/01621459.2013.849605>, Zhang W. et al
    (2017) <doi:10.1109/ICDMW.2017.44>, Arlot S. et al (2019). Two methods make
    use of dynamic programming and pruning, with no distributional assumptions
    other than the existence of certain absolute moments in one method.
    Hierarchical and exact search methods are included. All methods return the
    set of estimated change-points as well as other summary information."""

    homepage = "https://cloud.r-project.org/package=ecp"
    url      = "https://cloud.r-project.org/src/contrib/ecp_3.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ecp"

    version('3.1.3', sha256='a80ab10bafe30cc96287b9220e44c4b4eda40f5dd0546e4d2a2e1baab514c058')
    version('3.1.1', sha256='d2ab194e22e6ab0168222fbccfcf2e25c6cd51a73edc959086b0c6e0a7410268')

    depends_on('r@3.00:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
