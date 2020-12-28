# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRpart(RPackage):
    """Recursive partitioning for classification, regression and
    survival trees."""

    homepage = "https://cloud.r-project.org/package=rpart"
    url      = "https://cloud.r-project.org/src/contrib/rpart_4.1-10.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rpart"

    version('4.1-15', sha256='2b8ebe0e9e11592debff893f93f5a44a6765abd0bd956b0eb1f70e9394cfae5c')
    version('4.1-13', sha256='8e11a6552224e0fbe23a85aba95acd21a0889a3fe48277f3d345de3147c7494c')
    version('4.1-11', sha256='38ab80959f59bcdd2c4c72860e8dd0deab0307668cbbf24f96014d7a2496ad98')
    version('4.1-10', sha256='c5ddaed288d38118876a94c7aa5000dce0070b8d736dba12de64a9cb04dc2d85')

    depends_on('r@2.15.0:', type=('build', 'run'))
