# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lmdb(MakefilePackage):
    """Symas LMDB is an extraordinarily fast, memory-efficient database we
    developed for the Symas OpenLDAP Project. With memory-mapped files, it
    has the read performance of a pure in-memory database while retaining
    the persistence of standard disk-based databases."""

    homepage = "https://lmdb.tech/"
    url      = "https://github.com/LMDB/lmdb/archive/LMDB_0.9.21.tar.gz"

    version('0.9.24', sha256='44602436c52c29d4f301f55f6fd8115f945469b868348e3cddaf91ab2473ea26')
    version('0.9.22', sha256='f3927859882eb608868c8c31586bb7eb84562a40a6bf5cc3e13b6b564641ea28')
    version('0.9.21', sha256='1187b635a4cc415bb6972bba346121f81edd996e99b8f0816151d4090f90b559')
    version('0.9.16', sha256='49d7b40949f2ced9bc8b23ea6a89e75471a1c9126537a8b268c318a00b84322b')

    build_directory = 'libraries/liblmdb'

    @property
    def install_targets(self):
        return ['prefix={0}'.format(self.prefix), 'install']

    @run_after('install')
    def install_pkgconfig(self):
        mkdirp(self.prefix.lib.pkgconfig)

        with open(join_path(self.prefix.lib.pkgconfig, 'lmdb.pc'), 'w') as f:
            f.write('prefix={0}\n'.format(self.prefix))
            f.write('exec_prefix=${prefix}\n')
            f.write('libdir={0}\n'.format(self.prefix.lib))
            f.write('includedir={0}\n'.format(self.prefix.include))
            f.write('\n')
            f.write('Name: LMDB\n')
            f.write('Description: Symas LMDB is an extraordinarily fast, '
                    'memory-efficient database.\n')
            f.write('Version: {0}\n'.format(self.spec.version))
            f.write('Cflags: -I${includedir}\n')
            f.write('Libs: -L${libdir} -llmdb\n')
