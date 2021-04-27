# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RPs(RPackage):
    """List, Query, Manipulate System Processes

    List, query and manipulate all system processes, on 'Windows', 'Linux' and
    'macOS'."""

    homepage = "https://github.com/r-lib/ps"
    url      = "https://cloud.r-project.org/src/contrib/ps_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ps"

    version('1.5.0', sha256='7461a196f55557feda569a9791ad851c884f9a2dd71671655ed17cb048fafe96')
    version('1.3.0', sha256='289193d0ccd2db0b6fe8702e8c5711e935219b17f90f01a6e9684982413e98d1')
    version('1.2.1', sha256='bd7207164e6557a9e4213c4b00dc5dc23d7705ab290569765998640b16a3beff')
    version('1.1.0', sha256='5d5240d5bf1d48c721b3fdf47cfc9dbf878e388ea1f057b764db05bffdc4a9fe')
    version('1.0.0', sha256='9bdaf64aaa44ae11866868402eb75bf56c2e3022100476d9b9dcd16ca784ffd8')

    depends_on('r@3.1:', type=('build', 'run'))
