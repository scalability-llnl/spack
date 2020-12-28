# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRunit(RPackage):
    """RUnit: R Unit Test Framework"""

    homepage = "https://cloud.r-project.org/package=RUnit"
    url      = "https://cloud.r-project.org/src/contrib/RUnit_0.4.32.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RUnit/"

    version('0.4.32', sha256='23a393059989000734898685d0d5509ece219879713eb09083f7707f167f81f1')

    depends_on('r@2.5.0:', type=('build', 'run'))
