# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTruncdist(RPackage):
    """truncdist: Truncated Random Variables"""

    homepage = "https://cloud.r-project.org/package=truncdist"
    url      = "https://cloud.r-project.org/src/contrib/truncdist_1.0-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/truncdist"

    version('1.0-2', sha256='b848b68bdd983bd496fa7327632ffa8add8d2231229b8af5c8bc29d823e1300a')

    depends_on('r@2.0.1:', type=('build', 'run'))
    depends_on('r-evd', type=('build', 'run'))
