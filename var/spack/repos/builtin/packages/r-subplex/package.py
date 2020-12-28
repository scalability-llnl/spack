# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSubplex(RPackage):
    """Unconstrained Optimization using the Subplex Algorithm"""

    homepage = "https://cloud.r-project.org/package=subplex"
    url      = "https://cloud.r-project.org/src/contrib/subplex_1.4-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/subplex"

    version('1.5-4', sha256='ff94cf6b1560f78c31712c05bc2bc1b703339e09c7fc777ee94abf15fa7a8b81')
    version('1.5-2', sha256='6f8c3ccadf1ccd7f11f3eae28cec16eed3695f14e351b864d807dbaba6cd3ded')
    version('1.4-1', sha256='94b7b961aaa229a6f025151191ed50272af1394be69f1c41146b9e8c786caec6')

    depends_on('r@2.5.1:', type=('build', 'run'))
