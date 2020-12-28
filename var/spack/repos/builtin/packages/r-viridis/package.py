# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RViridis(RPackage):
    """viridis: Default Color Maps from 'matplotlib'"""

    homepage = "https://github.com/sjmgarnier/viridis"
    url      = "https://cloud.r-project.org/src/contrib/viridis_0.4.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/viridis"

    version('0.5.1', sha256='ddf267515838c6eb092938133035cee62ab6a78760413bfc28b8256165701918')
    version('0.5.0', sha256='fea477172c1e11be40554545260b36d6ddff3fe6bc3bbed87813ffb77c5546cd')
    version('0.4.0', sha256='93d2ded68ed7cec5633c260dbc47051416147aae074f29ebe135cc329250b00e')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-viridislite@0.3.0:', type=('build', 'run'))
    depends_on('r-ggplot2@1.0.1:', type=('build', 'run'))
    depends_on('r-gridextra', type=('build', 'run'))
