# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RParty(RPackage):
    """A Laboratory for Recursive Partytioning

    A computational toolbox for recursive partitioning. The core of the package
    is ctree(), an implementation of conditional inference trees which embed
    tree-structured  regression models into a well defined theory of
    conditional inference procedures. This non-parametric class of regression
    trees is applicable to all kinds of regression problems, including nominal,
    ordinal, numeric, censored as well as multivariate response variables and
    arbitrary measurement scales of the covariates.  Based on conditional
    inference trees, cforest() provides an implementation of Breiman's random
    forests. The function mob() implements an algorithm for recursive
    partitioning based on parametric models (e.g. linear models, GLMs or
    survival regression) employing parameter instability tests for split
    selection. Extensible functionality for visualizing tree-structured
    regression models is available. The methods are described in Hothorn et al.
    (2006) <doi:10.1198/106186006X133933>, Zeileis et al. (2008)
    <doi:10.1198/106186008X319331> and  Strobl et al. (2007)
    <doi:10.1186/1471-2105-8-25>."""

    homepage = "https://cloud.r-project.org/package=party"
    url      = "https://cloud.r-project.org/src/contrib/party_1.1-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/party"

    version('1.3-5', sha256='1c3a35d3fe56498361542b3782de2326561c14a8fa1b76f3c9f13beb1fd51364')
    version('1.3-3', sha256='9f72eea02d43a4cee105790ae7185b0478deb6011ab049cc9d31a0df3abf7ce9')
    version('1.3-2', sha256='9f350fa21114151c49bccc3d5f8536dbc5a608cfd88f60461c9805a4c630510b')
    version('1.1-2', sha256='c3632b4b02dc12ec949e2ee5b24004e4a4768b0bc9737432e9a85acbc2ed0e74')

    depends_on('r@2.14.0:', when='@:1.2-2', type=('build', 'run'))
    depends_on('r@3.0.0:', when='@1.2-3:', type=('build', 'run'))
    depends_on('r-mvtnorm@1.0-2:', type=('build', 'run'))
    depends_on('r-modeltools@0.2-21:', type=('build', 'run'))
    depends_on('r-strucchange', type=('build', 'run'))
    depends_on('r-survival@2.37-7:', type=('build', 'run'))
    depends_on('r-coin@1.1-0:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-sandwich@1.1-1:', type=('build', 'run'))
