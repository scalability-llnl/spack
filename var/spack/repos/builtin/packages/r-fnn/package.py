# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFnn(RPackage):
    """Cover-tree and kd-tree fast k-nearest neighbor search algorithms and
    related applications including KNN classification, regression and
    information measures are implemented."""

    homepage = "https://cloud.r-project.org/package=FNN"
    url      = "https://cloud.r-project.org/src/contrib/FNN_1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/FNN"

    version('1.1.3', sha256='de763a25c9cfbd19d144586b9ed158135ec49cf7b812938954be54eb2dc59432')
    version('1.1.2.2', sha256='b51a60fbbeff58c48cc90c2023c48972d5082d68efd02284c17ccd9820986326')
    version('1.1',   sha256='b2a2e97af14aa50ef4dce15a170e1d7329aebb7643bab4a6cf35609555acccce')
    version('1.0',   sha256='5606cc656c5488b56ee9227088bec662539589fd626ea5aae0e4d57d70a6fe03')
    version('0.6-4', sha256='2d0eb7b2aab9ff2e4deaf0b5e39b817f3f3701c0dcefa8a380bdc7111e68d853')
    version('0.6-3', sha256='9ac1817852427a056b5c6ad6ac5212bc43abd29ce15f98441a6261b25cf5f810')
    version('0.6-2', sha256='f1fc410c341175bdb11a75b063c8c987e15b632378b56148d3566b91fca53a31')

    depends_on('r@3.0.0:', type=('build', 'run'))
