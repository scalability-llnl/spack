##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import shutil
import copy

from spack import *


class Cp2k(Package):
    """CP2K is a quantum chemistry and solid state physics software package
    that can perform atomistic simulations of solid state, liquid, molecular,
    periodic, material, crystal, and biological systems
    """
    homepage = 'https://www.cp2k.org'
    url = 'https://sourceforge.net/projects/cp2k/files/cp2k-3.0.tar.bz2'

    version('4.1', 'b0534b530592de15ac89828b1541185e')
    version('3.0', 'c05bc47335f68597a310b1ed75601d35')

    variant('mpi', default=True, description='Enable MPI support')
    variant('plumed', default=False, description='Enable PLUMED support')

    depends_on('python', type='build')

    depends_on('lapack')
    depends_on('blas')
    depends_on('fftw')
    depends_on('libint@:1.2', when='@3.0,4.1')

    depends_on('mpi@2:', when='+mpi')
    depends_on('scalapack', when='+mpi')
    depends_on('plumed+shared+mpi', when='+plumed+mpi')
    depends_on('plumed+shared~mpi', when='+plumed~mpi')
    depends_on('pexsi+fortran', when='+mpi')

    # Apparently cp2k@4.1 needs an "experimental" version of libwannier.a
    # which is only available contacting the developer directly. See INSTALL
    # in the stage of cp2k@4.1
    depends_on('wannier90', when='@3.0+mpi')
    depends_on('elpa', when='+mpi')

    # TODO : add dependency on libsmm, libxsmm
    # TODO : add dependency on CUDA

    parallel = False

    def install(self, spec, prefix):
        # Construct a proper filename for the architecture file
        cp2k_architecture = '{0.architecture}-{0.compiler.name}'.format(spec)
        cp2k_version = 'sopt' if '~mpi' in spec else 'popt'
        makefile_basename = '.'.join([cp2k_architecture, cp2k_version])
        makefile = join_path('arch', makefile_basename)

        # Write the custom makefile
        with open(makefile, 'w') as mkf:
            # Optimization flags
            optflags = {
                'gcc': ['-O2',
                        '-ffast-math',
                        '-ftree-vectorize',
                        '-funroll-loops',
                        '-mtune=native'],
                'intel': ['-O2',
                          '-pc64',
                          '-unroll']
            }

            dflags = ['-DNDEBUG']

            cppflags = [
                '-D__FFTW3',
                '-D__LIBINT',
                '-D__LIBINT_MAX_AM=6',
                '-D__LIBDERIV_MAX_AM1=5',
                spec['fftw'].headers.cpp_flags
            ]

            if '^mpi@3:' in spec:
                cppflags.append('-D__MPI_VERSION=3')
            elif '^mpi@2:' in spec:
                cppflags.append('-D__MPI_VERSION=2')

            if '^intel-mkl' in spec:
                cppflags.append('-D__FFTSG')

            cflags = copy.deepcopy(optflags[self.spec.compiler.name])
            cxxflags = copy.deepcopy(optflags[self.spec.compiler.name])
            fcflags = copy.deepcopy(optflags[self.spec.compiler.name])
            fcflags.extend([
                '-ffree-form',
                '-ffree-line-length-none',
                spec['fftw'].headers.cpp_flags
            ])

            if '%intel' in spec:
                cflags.append('-fp-model precise')
                cxxflags.append('-fp-model precise')
                fcflags.extend(['-fp-model source', '-heap-arrays 64'])

            fftw = find_libraries('libfftw3', root=spec['fftw'].prefix.lib)
            ldflags = [fftw.search_flags]

            if 'superlu-dist@4.3' in spec:
                ldflags = ['-Wl,--allow-multiple-definition'] + ldflags

            libs = [
                join_path(spec['libint'].prefix.lib, 'libint.so'),
                join_path(spec['libint'].prefix.lib, 'libderiv.so'),
                join_path(spec['libint'].prefix.lib, 'libr12.so')
            ]

            if '+plumed' in self.spec:
                # Include Plumed.inc in the Makefile
                mkf.write('include {0}\n'.format(
                    join_path(self.spec['plumed'].prefix.lib,
                              'plumed',
                              'src',
                              'lib',
                              'Plumed.inc')
                ))
                # Add required macro
                dflags.extend(['-D__PLUMED2'])
                cppflags.extend(['-D__PLUMED2'])
                libs.extend([
                    join_path(self.spec['plumed'].prefix.lib,
                              'libplumed.{0}'.format(dso_suffix))
                ])

            mkf.write('CC = {0.compiler.cc}\n'.format(self))
            if '%intel' in self.spec:
                # CPP is a commented command in Intel arch of CP2K
                # This is the hack through which cp2k developers avoid doing :
                #
                # ${CPP} <file>.F > <file>.f90
                #
                # and use `-fpp` instead
                mkf.write('CPP = # {0.compiler.cc} -P\n\n'.format(self))
                mkf.write('AR = xiar -r\n\n')
            else:
                mkf.write('CPP = {0.compiler.cc} -E\n\n'.format(self))
                mkf.write('AR = ar -r\n\n')
            fc = self.compiler.fc if '~mpi' in spec else self.spec['mpi'].mpifc
            mkf.write('FC = {0}\n'.format(fc))
            mkf.write('LD = {0}\n'.format(fc))
            # Intel
            if '%intel' in self.spec:
                cppflags.extend([
                    '-D__INTEL',
                    '-D__HAS_ISO_C_BINDING',
                    '-D__USE_CP2K_TRACE',
                    '-D__MKL'
                ])
                fcflags.extend([
                    '-diag-disable 8290,8291,10010,10212,11060',
                    '-free',
                    '-fpp'
                ])
            # MPI
            if '+mpi' in self.spec:
                cppflags.extend([
                    '-D__parallel',
                    '-D__LIBPEXSI',
                    '-D__ELPA3',
                    '-D__SCALAPACK'
                ])
                if 'wannier90' in spec:
                    cppflags.append('-D__WANNIER90')

                fcflags.extend([
                    # spec['elpa:fortran'].headers.cpp_flags
                    '-I' + join_path(
                        spec['elpa'].prefix,
                        'include',
                        'elpa-{0}'.format(str(spec['elpa'].version)),
                        'modules'
                    ),
                    # spec[pexsi:fortran].headers.cpp_flags
                    '-I' + join_path(spec['pexsi'].prefix, 'fortran')
                ])
                scalapack = spec['scalapack'].libs
                ldflags.append(scalapack.search_flags)
                libs.extend([
                    join_path(spec['elpa'].prefix.lib,
                              'libelpa.{0}'.format(dso_suffix)),
                    join_path(spec['pexsi'].prefix.lib, 'libpexsi.a'),
                    join_path(spec['superlu-dist'].prefix.lib,
                              'libsuperlu_dist.a'),
                    join_path(
                        spec['parmetis'].prefix.lib,
                        'libparmetis.{0}'.format(dso_suffix)
                    ),
                    join_path(
                        spec['metis'].prefix.lib,
                        'libmetis.{0}'.format(dso_suffix)
                    ),
                ])

                if 'wannier90' in spec:
                    wannier = join_path(
                        spec['wannier90'].prefix.lib, 'libwannier.a'
                    )
                    libs.append(wannier)

                libs.extend(scalapack)
                libs.extend(self.spec['mpi:cxx'].libs)
                libs.extend(self.compiler.stdcxx_libs)
            # LAPACK / BLAS
            lapack = spec['lapack'].libs
            blas = spec['blas'].libs

            ldflags.append((lapack + blas).search_flags)
            libs.extend([str(x) for x in (fftw, lapack, blas)])

            dflags.extend(cppflags)
            cflags.extend(cppflags)
            cxxflags.extend(cppflags)
            fcflags.extend(cppflags)

            # Write compiler flags to file
            mkf.write('DFLAGS = {0}\n\n'.format(' '.join(dflags)))
            mkf.write('CPPFLAGS = {0}\n\n'.format(' '.join(cppflags)))
            mkf.write('CFLAGS = {0}\n\n'.format(' '.join(cflags)))
            mkf.write('CXXFLAGS = {0}\n\n'.format(' '.join(cxxflags)))
            mkf.write('FCFLAGS = {0}\n\n'.format(' '.join(fcflags)))
            mkf.write('LDFLAGS = {0}\n\n'.format(' '.join(ldflags)))
            if '%intel' in spec:
                mkf.write('LDFLAGS_C = {0}\n\n'.format(
                    ' '.join(ldflags) + ' -nofor_main')
                )
            mkf.write('LIBS = {0}\n\n'.format(' '.join(libs)))

        with working_dir('makefiles'):
            # Apparently the Makefile bases its paths on PWD
            # so we need to set PWD = os.getcwd()
            pwd_backup = env['PWD']
            env['PWD'] = os.getcwd()
            make('ARCH={0}'.format(cp2k_architecture),
                 'VERSION={0}'.format(cp2k_version))
            env['PWD'] = pwd_backup
        exe_dir = join_path('exe', cp2k_architecture)
        shutil.copytree(exe_dir, self.prefix.bin)
