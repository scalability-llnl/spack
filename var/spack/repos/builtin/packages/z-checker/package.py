# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------

from spack.package import *


class ZChecker(AutotoolsPackage):
    """a library to perform the compression assessment for lossy compressors"""

    homepage = "https://github.com/CODARcode/Z-checker"
    url      = "https://github.com/CODARcode/Z-checker/releases/download/0.5.0/Z-checker-0.5.0.tar.gz"

    maintainers = ['disheng222']

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
