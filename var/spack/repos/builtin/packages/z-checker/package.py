# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------

from spack import *


class ZChecker(AutotoolsPackage):
    """a library to perform the compression assessment for lossy compressors"""

    homepage = "https://github.com/CODARcode/Z-checker"
    url      = "https://github.com/CODARcode/Z-checker/releases/download/0.6.0/Z-checker-0.6.0.tar.gz"
    git      = "https://github.com/CODARcode/Z-checker"
    maintainers = ['disheng222']

    version('0.6.0', sha256='b01c2c78157234a734c2f4c10a7ab82c329d3cd1a8389d597e09386fa33a3117')
    version('0.5.0', sha256='ad5e68472c511b393ee1ae67d2e3072a22004001cf19a14bd99a2e322a6ce7f9')

    variant('mpi', default=False,
            description='Enable mpi compilation')

    depends_on('mpi', when="+mpi")

    def configure_args(self):
        args = []
        if '+mpi' in self.spec:
            args += ['--enable-mpi']
        else:
            args += ['--disable-mpi']
        return args
 
    def url_for_version(self, version):
        """provide url to ensure that download counting via github releases
        works accurately"""
        url = "https://github.com/CODARcode/Z-checker/releases/download/{0}/Z-checker-{0}.tar.gz"
        return url.format(version)
