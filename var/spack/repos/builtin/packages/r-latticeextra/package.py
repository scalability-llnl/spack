# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLatticeextra(RPackage):
    """Building on the infrastructure provided by the lattice package,
    this package provides several new high-level functions and methods,
    as well as additional utilities such as panel and axis annotation
    functions."""

    homepage = "http://latticeextra.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/latticeExtra_0.6-28.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/latticeExtra"

    version('0.6-28', sha256='780695323dfadac108fb27000011c734e2927b1e0f069f247d65d27994c67ec2')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
