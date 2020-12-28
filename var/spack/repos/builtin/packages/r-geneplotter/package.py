# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeneplotter(RPackage):
    """Graphics related functions for Bioconductor."""

    homepage = "https://bioconductor.org/packages/geneplotter"
    git      = "https://git.bioconductor.org/packages/geneplotter.git"

    version('1.62.0', commit='1fbaddde11014b453b131860409f89cd784e8e48')
    version('1.60.0', commit='6723a9fc0730e146187e79c2ddab6a68186dc5ad')
    version('1.58.0', commit='2b3f44804d61a40cfe7eaedf74ac9f5a054f7fde')
    version('1.56.0', commit='881d25aece3dc00cc4280457ffecdc25e93bb1f1')
    version('1.54.0', commit='efdd946e092e44e35fde1eb4bcc5ec1d52090940')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-annotate', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
