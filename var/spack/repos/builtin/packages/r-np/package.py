# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNp(RPackage):
    """This package provides a variety of nonparametric (and semiparametric)
    kernel methods that seamlessly handle a mix of continuous, unordered, and
    ordered factor data types. We would like to gratefully acknowledge support
    from the Natural Sciences and Engineering Research Council of Canada
    (NSERC:www.nserc.ca), the Social Sciences and Humanities Research Council
    of Canada (SSHRC:www.sshrc.ca), and the Shared Hierarchical Academic
    Research Computing Network (SHARCNET:www.sharcnet.ca)."""

    homepage = "https://github.com/JeffreyRacine/R-Package-np/"
    url      = "https://cloud.r-project.org/src/contrib/np_0.60-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/np"

    version('0.60-9', sha256='fe31a8985f0b1a576a7775022b7131093b1c9a8337734136d5fcad85fa6592fc')
    version('0.60-8', sha256='924c342feb2a862fa3871a45db5f8434dbbfb900cfc40c001a0872108a3a069e')
    version('0.60-2', sha256='25d667fc1056899516584b9d5d933377e6f4694d8e5e868dd047db572b69417f')

    depends_on('r-boot', type=('build', 'run'))
    depends_on('r-cubature', type=('build', 'run'))
    depends_on('r-quadprog', when='@0.60-8:', type=('build', 'run'))
    depends_on('r-quantreg', when='@0.60-8:', type=('build', 'run'))
