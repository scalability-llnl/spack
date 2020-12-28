# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCtc(RPackage):
    """Cluster and Tree Conversion..

       Tools for export and import classification trees and clusters to other
       programs"""

    homepage = "https://bioconductor.org/packages/ctc"
    git      = "https://git.bioconductor.org/packages/ctc.git"

    version('1.58.0', commit='c41df03ac149db20c5e337142142d61cfb9b43fb')
    version('1.56.0', commit='cbd5befdda4630799f8fe0d868d83b094e3d352f')
    version('1.54.0', commit='0c3df81dfc8fabe12e11884bed44b64e11fd6d4e')
    version('1.52.0', commit='ffff8693cab5ebad610d139367f089418f1830a1')
    version('1.50.0', commit='4ee7519c3e5172e140c2658b4cf5271d229acc7e')

    depends_on('r-amap', type=('build', 'run'))
