# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Minimap2(PythonPackage):
    """Minimap2 is a versatile sequence alignment program that aligns DNA or
       mRNA sequences against a large reference database.
       Mappy provides a convenient interface to minimap2."""

    homepage = "https://github.com/lh3/minimap2"
    url      = "https://github.com/lh3/minimap2/releases/download/v2.2/minimap2-2.2.tar.bz2"

    version('2.14', sha256='9088b785bb0c33488ca3a27c8994648ce21a8be54cb117f5ecee26343facd03b')
    version('2.10', sha256='52b36f726ec00bfca4a2ffc23036d1a2b5f96f0aae5a92fd826be6680c481c20')
    version('2.2', sha256='7e8683aa74c4454a8cfe3821f405c4439082e24c152b4b834fdb56a117ecaed9')

    conflicts('target=aarch64:', when='@:2.10')
    depends_on('zlib', type='link')
    depends_on('py-cython', type='build')

    @run_after('install')
    def install_minimap2(self):
        make_arg = []
        if self.spec.target.family == 'aarch64':
            make_arg.extend([
                'arm_neon=1',
                'aarch64=1'
            ])
        make(*make_arg)
        mkdirp(prefix.bin)
        install('minimap2', prefix.bin)
