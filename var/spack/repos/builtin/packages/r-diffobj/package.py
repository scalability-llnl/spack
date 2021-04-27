# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RDiffobj(RPackage):
    """Diffs for R Objects

    Generate a colorized diff of two R objects for an intuitive visualization
    of their differences."""

    homepage = "https://github.com/brodieG/diffobj"
    url      = "https://cloud.r-project.org/src/contrib/diffobj_0.3.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/diffobj"

    version('0.3.3', sha256='414e5573470b9565b9149a0a61c7e8344fb37f889d23dc4e131acc8aa62e6df4')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-crayon@1.3.2:', type=('build', 'run'))
