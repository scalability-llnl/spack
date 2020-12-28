# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Portcullis(AutotoolsPackage):
    """PORTable CULLing of Invalid Splice junctions"""

    homepage = "https://github.com/maplesond/portcullis"
    url      = "https://github.com/maplesond/portcullis/archive/Release-1.1.2.tar.gz"

    version('1.1.2', sha256='5c581a7f827ffeecfe68107b7fe27ed60108325fd2f86a79d93f61b328687749')

    depends_on('autoconf@2.53:', type='build')
    depends_on('automake@1.11:', type='build')
    depends_on('libtool@2.4.2:',  type='build')
    depends_on('m4', type='build')

    depends_on('zlib', type='build')
    depends_on('samtools', type='build')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))

    # later versions of py-sphinx don't get detected by the configure script
    depends_on('py-sphinx@1.3:1.4')

    def patch(self):
        # remove static linking to libstdc++
        filter_file(
            'AM_LDFLAGS="-static-libstdc++"',
            'AM_LDFLAGS=""',
            'configure.ac', string=True
        )

        # prevent install scripts from ruining our PYTHONPATH
        filter_file(
            'export PYTHONPATH=$(DESTDIR)$(pythondir)',
            'export PYTHONPATH="$(PYTHONPATH):$(DESTDIR)$(pythondir)"',
            'scripts/Makefile.am', string=True
        )

        # remove -m64 on aarch64
        if self.spec.target.family == 'aarch64':
            for f in ['lib/Makefile.am', 'src/Makefile.am']:
                filter_file('-m64', '', f)

    def build(self, spec, prefix):
        # build manpages
        make('man')

        # run boost build script
        sh = which('sh')
        sh('build_boost.sh')
