# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Openmx(MakefilePackage):
    """OpenMX (Open source package for Material eXplorer) is a software
       package for nano-scale material simulations based on density functional
       theories (DFT), norm-conserving pseudopotentials, and pseudo-atomic
       localized basis functions."""

    homepage = "http://www.openmx-square.org/index.html"
    url      = "http://t-ozaki.issp.u-tokyo.ac.jp/openmx3.8.tar.gz"

    version('3.8', sha256='36ee10d8b1587b25a2ca1d57f110111be65c4fb4dc820e6d93e1ed2b562634a1')

    resource(name='patch',
             url='http://www.openmx-square.org/bugfixed/18June12/patch3.8.5.tar.gz',
             sha256='d0fea2ce956d796a87a4bc9e9d580fb115ff2a22764650fffa78bb79a1b30468',
             placement='patch',
             when='@3.8')

    depends_on('mpi')
    depends_on('fftw')
    depends_on('blas')
    depends_on('lapack')

    parallel = False

    phases = ['edit', 'build']

    def edit(self, spec, prefix):
        # Move contents to source/
        # http://www.openmx-square.org/bugfixed/18June12/README.txt
        copy_tree('patch', 'source')

        makefile = FileFilter('./source/makefile')
        makefile.filter('^DESTDIR.*$', 'DESTDIR = {0}/bin'.format(prefix))

    def build(self, spec, prefix):
        mkdirp(prefix.bin)
        lapack_blas_libs = spec['lapack'].libs + spec['blas'].libs
        lapack_blas_headers = spec['lapack'].headers + spec['blas'].headers

        common_option = []
        cc_option = [spec['mpi'].mpicc,
                     self.compiler.openmp_flag,
                     spec['fftw'].headers.include_flags,
                     ]
        fc_option = [spec['mpi'].mpifc]
        lib_option = [spec['fftw'].libs.ld_flags,
                      lapack_blas_libs.ld_flags,
                      '-lmpi_mpifh',
                      ]

        if '%fj' in spec:
            common_option.append('-Dkcomp  -Kfast')
            cc_option.append('-Dnosse -Nclang')
            fc_option.append(self.compiler.openmp_flag)
        else:
            common_option.append('-O3')
            common_option.append(lapack_blas_headers.include_flags)
            if '%gcc' in spec:
                lib_option.append('-lgfortran')

        with working_dir('source'):
            make('all',
                 'CC={0} {1} -I$(LIBERIDIR)'
                 .format(' '.join(cc_option), ' '.join(common_option)),
                 'FC={0} {1}'
                 .format(' '.join(fc_option), ' '.join(common_option)),
                 'LIB={0}'.format(' '.join(lib_option)),
                 )
