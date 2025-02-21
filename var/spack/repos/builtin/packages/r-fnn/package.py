# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFnn(RPackage):
    """Fast Nearest Neighbor Search Algorithms and Applications.

    Cover-tree and kd-tree fast k-nearest neighbor search algorithms and
    related applications including KNN classification, regression and
    information measures are implemented."""

    cran = "FNN"

    version("1.1.4", sha256="db4db5a348c6051fe547193c282b6e5cc839f68f51e0afccf4939f35e9a2fc27")
    version("1.1.3.2", sha256="d701a13487979ebb07a071f4cc83fcf4daea5832d1f3923bce1e0d671dfe0e87")
    version("1.1.3.1", sha256="52b0e20611481a95bced40be4126f44b002fd3a9c4c9674bb34db4e1e3b5be5a")
    version("1.1.3", sha256="de763a25c9cfbd19d144586b9ed158135ec49cf7b812938954be54eb2dc59432")
    version("1.1.2.2", sha256="b51a60fbbeff58c48cc90c2023c48972d5082d68efd02284c17ccd9820986326")
    version("1.1", sha256="b2a2e97af14aa50ef4dce15a170e1d7329aebb7643bab4a6cf35609555acccce")
    version("1.0", sha256="5606cc656c5488b56ee9227088bec662539589fd626ea5aae0e4d57d70a6fe03")
    version("0.6-4", sha256="2d0eb7b2aab9ff2e4deaf0b5e39b817f3f3701c0dcefa8a380bdc7111e68d853")
    version("0.6-3", sha256="9ac1817852427a056b5c6ad6ac5212bc43abd29ce15f98441a6261b25cf5f810")
    version("0.6-2", sha256="f1fc410c341175bdb11a75b063c8c987e15b632378b56148d3566b91fca53a31")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.1.4:")
