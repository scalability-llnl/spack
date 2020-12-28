# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSquash(RPackage):
    """Color-Based Plots for Multivariate Visualization"""

    homepage = "https://cloud.r-project.org/package=squash"
    url      = "https://cloud.r-project.org/src/contrib/squash_1.0.8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/squash"

    version('1.0.8', sha256='e6932c0a461d5c85f7180a31d18a3eb4f28afd6769efe251075a4de12de039f4')
    version('1.0.7', sha256='d2d7182a72dfd93b8b65e775bea11e891c38598fa49a3ed4f92ec1159ffab6f1')
