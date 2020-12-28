# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qbox(MakefilePackage):
    """Qbox is a C++/MPI scalable parallel implementation of first-principles
    molecular dynamics (FPMD) based on the plane-wave, pseudopotential
    formalism. Qbox is designed for operation on large parallel computers."""

    homepage = "http://qboxcode.org/"
    url      = "http://qboxcode.org/download/qbox-1.63.7.tgz"

    version('1.63.7', sha256='40acf4535c4dcab16066c218b1c2a083c238a1f54c43a1d2d4afcefb578086ed')
    version('1.63.5', sha256='fa6d0e41622690f14b7cd0c2735d3d8d703152eb2c51042cdd77a055926cd90a')
    version('1.63.4', sha256='829ae57e43ecb79f7dca8fb02aa70c85b0bbb68684a087d3cd1048b50fbc8e96')
    version('1.63.2', sha256='17873414fed5298b6a4b66ae659ea8348119238b36b532df8a7c8fca0ed4eada')
    version('1.63.0', sha256='8ad0727e4ebe709b2647a281756675e4840b3f29799f7169f79a9100c6538d31')
    version('1.62.3', sha256='e82df8307d038af75471f22d9449a5f5e2ad00bb34a89b1b2c25cc65da83c9b5')
    version('1.60.9', sha256='d82434031ab8214879274eb6f8674c6004b65ad5f9a07635101b82300af6d43c')
    version('1.60.4', sha256='7707a3bbecb05864e651d4f8885685299edd8f95fcd300dc401ff6652e85a351')
    version('1.60.0', sha256='802b531c7fe67d8fad27618911b2e158f7c69099677c0e08202dca24f81e10fd')
    version('1.58.0', sha256='662f55adedfe1154f8affd060b4f846cd37751f020fe854ef560aeb435fd0312')
    version('1.56.2', sha256='63df818e071cfc826645ee266a239a0cc00cea874d266f572fc20b1e2db7b351')
    version('1.54.4', sha256='8f556fde5307b96ed03612b339f793fc2933841f91555b6e7000cbb003709b7a')
    version('1.54.2', sha256='45ef811c05c9224baee87626d5a5bae91008a8b117df7e964c5976f27e54e9e9')
    version('1.52.3', sha256='9424eaf56dbf33394674f0be76aecf76637702d060e45c5edc95d872a165cd42')
    version('1.52.2', sha256='39d892f1bacd355d6ab4dbdd0ee4303ac6916fa9decf0e828f16003e61d59798')
    version('1.50.4', sha256='2babf332132005dc93f280b274c68e8e44ecd8e2d1cf21cc91e212f17f8644a8')
    version('1.50.2', sha256='0defe312319ac460b5b667eca982e4cd6a23750e5bdaa214d1c127ce2aba0a21')
    version('1.50.1', sha256='114363654d7059662b0f3269615d0af1514298f4f488889d8e7ef8f1c4b8898d')
    version('1.47.0', sha256='5c45aa8f6b2f774c04423c50b4e340dc35ca1deb2826ead8f1a508cd027974a9')
    version('1.45.3', sha256='986e82a69f90a96cccd1a192921024ffdcefb3b86df361946d88b12669156a80')
    version('1.45.1', sha256='3cea45743c0cd24cd02865c39a360c55030dab0f4b9b7b46e615af9b3b65c1da')
    version('1.45.0', sha256='cc722641bf3c3a172bdb396216a945f2830cc64de60d716b7054145ba52ab431')
    version('1.44.0', sha256='f29cf2a727235d4fa6bded7725a1a667888ab103278e995c46dd754654f112f1')

    depends_on('mpi')
    depends_on('blas')
    depends_on('scalapack')
    depends_on('fftw')
    depends_on('xerces-c')
    depends_on('python@:2.999', type='run')
    depends_on('gnuplot', type='run')

    # Change /usr/bin/python shebangs to /usr/bin/env python
    patch('qbox-python-shebang-path.patch')

    build_directory = 'src'

    def edit(self, spec, prefix):
        with open('src/spack.mk', 'w') as mkfile:
            mkfile.write('CXX = {0}\n'.format(spec['mpi'].mpicxx))
            mkfile.write('LD = $(CXX)\n')
            qbox_libs = spec['fftw'].libs + spec['xerces-c'].libs + \
                spec['scalapack'].libs + spec['blas'].libs
            mkfile.write('LDFLAGS = {0}\n'.format(qbox_libs.ld_flags))
            mkfile.write('DFLAGS = {0}\n'.format(' -D'.join((
                '',
                '_LARGEFILE_SOURCE', 'USE_MPI', 'USE_XERCES',
                'XERCESC_3', 'MPICH_IGNORE_CXX_SEEK', 'SCALAPACK',
                'USE_FFTW3', 'FFTWMEASURE', 'FFTW3_2D', 'ADD_',
            ))))
            mkfile.write('CXXFLAGS = {0}\n'.format(' '.join((
                '-g', '-O3', '$(DFLAGS)',
            ))))
        filter_file('$(TARGET)', 'spack', 'src/Makefile', string=True)

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix.util)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('src/qb', prefix.bin)
        install_tree('test', prefix.test)
        install_tree('xml', prefix.xml)
        install_tree('util', prefix.util)
