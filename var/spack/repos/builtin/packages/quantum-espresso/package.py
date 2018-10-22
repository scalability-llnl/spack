##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import glob
import os.path

from spack import *


class QuantumEspresso(Package):
    """Quantum-ESPRESSO is an integrated suite of Open-Source computer codes
    for electronic-structure calculations and materials modeling at the
    nanoscale. It is based on density-functional theory, plane waves, and
    pseudopotentials.
    """

    homepage = 'http://quantum-espresso.org'
    url      = 'https://github.com/QEF/q-e/archive/qe-6.2.0.tar.gz'

    version('6.3',   '1b67687d90d1d16781d566d44d14634c')
    version('6.2.1', '769cc973382156bffd35254c3dbaf453')
    version('6.2.0', '972176a58d16ae8cf0c9a308479e2b97')
    version('6.1.0', '3fe861dcb5f6ec3d15f802319d5d801b')
    version('6.0.0', 'd915f2faf69d0e499f8e1681c42cbfc9')
    version('5.4',   '085f7e4de0952e266957bbc79563c54e')
    version('5.3',   'be3f8778e302cffb89258a5f936a7592')
    version('develop', git='https://github.com/QEF/q-e.git')

    variant('mpi', default=True, description='Builds with mpi support')
    variant('openmp', default=False, description='Enables openMP support')
    variant('scalapack', default=True, description='Enables scalapack support')
    variant('elpa', default=True, description='Uses elpa as an eigenvalue solver')

    # Support for HDF5 has been added starting in version 6.1.0 and is
    # still experimental, therefore we default to False for the variant
    variant('hdf5', default=False, description='Builds with HDF5 support')

    # Dependencies
    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')
    depends_on('scalapack', when='+scalapack+mpi')

    depends_on('fftw+mpi', when='+mpi')
    depends_on('fftw~mpi', when='~mpi')
    depends_on('elpa+openmp', when='+elpa+openmp')
    depends_on('elpa~openmp', when='+elpa~openmp')
    # Versions of HDF5 prior to 1.8.16 lead to QE runtim errors
    depends_on('hdf5@1.8.16:+fortran', when='+hdf5')

    patch('dspev_drv_elpa.patch', when='@6.1.0:+elpa ^elpa@2016.05.004')
    patch('dspev_drv_elpa.patch', when='@6.1.0:+elpa ^elpa@2016.05.003')

    # Conflicts
    # MKL with 64-bit integers not supported.
    conflicts('intel-mkl+ilp64')

    # Supporting the FFTW3 interface in old versions of MKL is difficult.
    conflicts('intel-mkl@:11.3.2.210')

    # External FFTW2 is not supported out of the box.
    conflicts('fftw@2.1.5')

    # We can't ask for scalapack or elpa if we don't want MPI
    conflicts(
        '+scalapack',
        when='~mpi',
        msg='scalapack is a parallel library and needs MPI support'
    )

    conflicts(
        '+elpa',
        when='~mpi',
        msg='elpa is a parallel library and needs MPI support'
    )

    # HDF5 support introduced in 6.1 but requires MPI, develop
    # branch and future releases will support serial HDF5
    conflicts('+hdf5', when='@:6.0.0')
    conflicts(
        '+hdf5',
        when='~mpi@6.1.0:6.3',
        msg='HDF5 support only available with MPI for QE 6.1:6.3'
    )

    # Elpa is formally supported by @:5.4.0, but QE configure searches
    # for it in the wrong folders (or tries to download it within
    # the build directory). Instead of patching Elpa to provide the
    # folder QE expects as a link, we issue a conflict here.
    conflicts('+elpa', when='@:5.4.0')

    # Spurious problems running in parallel the Makefile
    # generated by the configure
    parallel = False

    # QE 6.3 `make install` broken and a patch must be applied
    patch_url = 'https://gitlab.com/QEF/q-e/commit/88e6558646dbbcfcafa5f3fa758217f6062ab91c.diff'
    patch_checksum = 'b776890d008e16cca28c31299c62f47de0ba606b900b17cbc27c041f45e564ca'
    patch(patch_url, sha256=patch_checksum, when='@6.3')

    def install(self, spec, prefix):

        prefix_path = prefix.bin if '@:5.4.0' in spec else prefix
        options = ['-prefix={0}'.format(prefix_path)]

        if '+mpi' in spec:
            mpi = spec['mpi']
            options.append('--enable-parallel=yes')
            options.append('MPIF90={0}'.format(mpi.mpifc))
        else:
            options.append('--enable-parallel=no')

        if '+openmp' in spec:
            options.append('--enable-openmp')


        # For Intel package, lapack.libs = blas.libs, hence it will appear
        # twice in in link line but this is harmless
        lapack_blas = spec['lapack'].libs + spec['blas'].libs

        # Based on the current QE configure scripts, LAPACK_LIBS
        # is not used for external LAPACK
        options.append('BLAS_LIBS={0}'.format(lapack_blas.ld_flags))

        if '+scalapack' in spec:
            scalapack_option = 'intel' if '^intel-mkl' in spec else 'yes'
            options.append('--with-scalapack={0}'.format(scalapack_option))

        if '+elpa' in spec:

            # Spec for elpa
            elpa = spec['elpa']

            # Find where the Fortran module resides
            elpa_module = find(elpa.prefix, 'elpa.mod')

            # Compute the include directory from there: versions
            # of espresso prior to 6.1 requires -I in front of the directory
            elpa_include = '' if '@6.1:' in spec else '-I'
            elpa_include += os.path.dirname(elpa_module[0])

            options.extend([
                '--with-elpa-include={0}'.format(elpa_include),
                '--with-elpa-lib={0}'.format(elpa.libs[0])
            ])

        if '+hdf5' in spec:
            options.append('--with-hdf5={0}'.format(spec['hdf5'].prefix))


        options.extend([
            'F77={0}'.format(env['SPACK_F77']),
            'F90={0}'.format(env['SPACK_FC']),
            'CC={0}'.format(env['SPACK_CC'])
        ])

        configure(*options)

        # Apparently the build system of QE is so broken that:
        #
        # 1. The variable reported on stdout as HDF5_LIBS is actually
        #    called HDF5_LIB (singular)
        # 2. The link flags omit a few `-L` from the line, and this
        #    causes the linker to break
        #
        # Below we try to match the entire HDF5_LIB line and substitute
        # with the list of libraries that needs to be linked.
        if '+hdf5' in spec:
            make_inc = join_path(self.stage.source_path, 'make.inc')
            hdf5_libs = ' '.join(spec['hdf5:hl,fortran'].libs)
            filter_file(
                'HDF5_LIB([\s]*)=([\s\w\-\/.,]*)',
                'HDF5_LIB = {0}'.format(hdf5_libs),
                make_inc
            )

        make('all')

        if 'platform=darwin' in spec:
            mkdirp(prefix.bin)
            for filename in glob.glob("bin/*.x"):
                install(filename, prefix.bin)
        else:
            make('install')
