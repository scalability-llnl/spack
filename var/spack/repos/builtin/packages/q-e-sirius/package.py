# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# adapted from official quantum espresso package
from spack.package import *


class QESirius(Package):
    """SIRIUS enabled fork of QuantumESPRESSO. """

    homepage = 'https://github.com/electronic-structure/q-e-sirius/'
    url = 'https://github.com/electronic-structure/q-e-sirius/archive/v6.5-rc4-sirius.tar.gz'
    git = 'https://github.com/electronic-structure/q-e-sirius.git'

    maintainers = ['simonpintarelli']

    version('develop', branch='ristretto')

    version('6.5-rc2-sirius', sha256='460b678406eec36e4ee828c027929cf8720c3965a85c20084c53398b123c9ae9')
    version('6.5-rc3-sirius', sha256='1bfb8c1bba815b5ab2d733f51a8f9aa7b079f2859e6f14e4dcda708ebf172b02')
    version('6.5-rc4-sirius', sha256='be5529d65e4b301d6a6d1235e8d88277171c1732768bf1cf0c7fdeae154c79f1')

    variant('mpi', default=True, description='Builds with mpi support')
    variant('openmp', default=True, description='Enables openMP support')
    variant('scalapack', default=True, description='Enables scalapack support')
    variant('elpa', default=False, description='Uses elpa as an eigenvalue solver')

    # Support for HDF5 has been added starting in version 6.1.0 and is
    # still experimental, therefore we default to False for the variant
    variant(
        'hdf5', default='none', description='Builds with HDF5 support',
        values=('parallel', 'serial', 'none'), multi=False
    )

    # Enables building Electron-phonon Wannier 'epw.x' executable
    # http://epw.org.uk/Main/About
    variant('epw', default=False,
            description='Builds Electron-phonon Wannier executable')

    # Apply upstream patches by default. Variant useful for 3rd party
    # patches which are incompatible with upstream patches
    desc = 'Apply recommended upstream patches. May need to be set '
    desc += 'to False for third party patches or plugins'
    variant('patch', default=True, description=desc)

    # QMCPACK converter patch
    # https://github.com/QMCPACK/qmcpack/tree/develop/external_codes/quantum_espresso
    variant('qmcpack', default=False,
            description='Build QE-to-QMCPACK wave function converter')

    # Dependencies
    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw-api@3')
    depends_on('sirius+fortran+shared')
    depends_on('mpi', when='+mpi')
    depends_on('scalapack', when='+scalapack+mpi')
    depends_on('elpa+openmp', when='+elpa+openmp')
    depends_on('elpa~openmp', when='+elpa~openmp')
    # Versions of HDF5 prior to 1.8.16 lead to QE runtime errors
    depends_on('hdf5@1.8.16:+fortran+hl+mpi', when='hdf5=parallel')
    depends_on('hdf5@1.8.16:+fortran+hl~mpi', when='hdf5=serial')
    depends_on('hdf5', when='+qmcpack')
    # TODO: enable building EPW when ~mpi
    depends_on('mpi', when='+epw')

    # CONFLICTS SECTION
    # Omitted for now due to concretizer bug
    # MKL with 64-bit integers not supported.
    # conflicts(
    #     '^mkl+ilp64',
    #     msg='Quantum ESPRESSO does not support MKL 64-bit integer variant'
    # )

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

    # HDF5 support introduced in 6.1.0, but the configure had some limitations.
    # In recent tests (Oct 2019), GCC and Intel work with the HDF5 Spack
    # package for the default variant. This is only for hdf5=parallel variant.
    # Support, for hdf5=serial was introduced in 6.4.1 but required a patch
    # for the serial (no MPI) case. This patch was to work around an issue
    # that only manifested itself inside the Spack environment.
    conflicts(
        'hdf5=parallel',
        when='@:6.0',
        msg='parallel HDF5 support only in QE 6.1.0 and later'
    )

    conflicts(
        'hdf5=serial',
        when='@:6.4.0',
        msg='serial HDF5 support only in QE 6.4.1 and later'
    )

    conflicts(
        'hdf5=parallel',
        when='~mpi',
        msg='parallel HDF5 requires MPI support'
    )

    # Elpa is formally supported by @:5.4.0, but QE configure searches
    # for it in the wrong folders (or tries to download it within
    # the build directory). Instead of patching Elpa to provide the
    # folder QE expects as a link, we issue a conflict here.
    conflicts('+elpa', when='@:5.4.0')

    # Some QMCPACK converters are incompatible with upstream patches.
    # HDF5 is a hard requirement. Need to do two HDF5 cases explicitly
    # since Spack lacks support for expressing NOT operation.
    conflicts(
        '@6.4+patch',
        when='+qmcpack',
        msg='QE-to-QMCPACK wave function converter requires '
        'deactivatation of upstream patches'
    )
    conflicts(
        '@6.3:6.4.0 hdf5=serial',
        when='+qmcpack',
        msg='QE-to-QMCPACK wave function converter only '
        'supported with parallel HDF5'
    )
    conflicts(
        'hdf5=none',
        when='+qmcpack',
        msg='QE-to-QMCPACK wave function converter requires HDF5'
    )

    # The first version of Q-E to feature integrated EPW is 6.0.0,
    # as per http://epw.org.uk/Main/DownloadAndInstall .
    # Complain if trying to install a version older than this.
    conflicts('+epw', when='@:5',
              msg='EPW only available from version 6.0.0 and on')

    # Below goes some constraints as shown in the link above.
    # Constraints may be relaxed as successful reports
    # of different compiler+mpi combinations arrive

    # TODO: enable building EPW when ~mpi
    conflicts('+epw', when='~mpi', msg='EPW needs MPI')

    # EPW doesn't gets along well with OpenMPI 2.x.x
    conflicts('+epw', when='^openmpi@2.0.0:2.999.999',
              msg='OpenMPI version incompatible with EPW')

    # EPW also doesn't gets along well with PGI 17.x + OpenMPI 1.10.7
    conflicts('+epw', when='^openmpi@1.10.7%pgi@17.0:17.12',
              msg='PGI+OpenMPI version combo incompatible with EPW')

    # Spurious problems running in parallel the Makefile
    # generated by the configure
    parallel = False

    def install(self, spec, prefix):

        prefix_path = prefix.bin if '@:5.4.0' in spec else prefix
        options = ['-prefix={0}'.format(prefix_path)]

        sirius = spec['sirius']
        options.append('LIBS={0}'.format(sirius.libs[0]))
        options.append('LD_LIBS={0}'.format(sirius.libs[0]))

        options.append('--disable-xml')

        # QE autoconf compiler variables has some limitations:
        # 1. There is no explicit MPICC variable so we must re-purpose
        #    CC for the case of MPI.
        # 2. F90 variable is set to be consistent with MPIF90 wrapper
        # 3. If an absolute path for F90 is set, the build system breaks.
        #
        # Thus, due to 2. and 3. the F90 variable is not explictly set
        # because it would be mostly pointless and could lead to erroneous
        # behaviour.
        if '+mpi' in spec:
            mpi = spec['mpi']
            options.append('--enable-parallel=yes')
            options.append('MPIF90={0}'.format(mpi.mpifc))
            options.append('CC={0}'.format(mpi.mpicc))
        else:
            options.append('--enable-parallel=no')
            options.append('CC={0}'.format(spack_cc))

        options.append('F77={0}'.format(spack_f77))
        options.append('F90={0}'.format(spack_fc))

        header_dir = sirius.headers.directories[0]
        f90flags = 'F90FLAGS=-cpp -I {0}/sirius'.format(header_dir)

        if self.spec.satisfies('%gcc@10:'):
            f90flags += ' -fallow-argument-mismatch'

        options.append(f90flags)

        if '+openmp' in spec:
            options.append('--enable-openmp')

        # QE external BLAS, FFT, SCALAPACK detection is a bit tricky.
        # More predictable to pass in the correct link line to QE.
        # If external detection of BLAS, LAPACK and FFT fails, QE
        # is supposed to revert to internal versions of these libraries
        # instead -- but more likely it will pickup versions of these
        # libraries found in its the system path, e.g. Red Hat or
        # Ubuntu's FFTW3 package.

        # FFT
        # FFT detection gets derailed if you pass into the CPPFLAGS, instead
        # you need to pass it in the FFTW_INCLUDE and FFT_LIBS directory.
        # QE supports an internal FFTW2, but only an external FFTW3 interface.

        if '^mkl' in spec:
            # A seperate FFT library is not needed when linking against MKL
            options.append(
                'FFTW_INCLUDE={0}'.format(join_path(env['MKLROOT'],
                                                    'include/fftw')))
        if '^fftw@3:' in spec:
            fftw_prefix = spec['fftw'].prefix
            options.append('FFTW_INCLUDE={0}'.format(fftw_prefix.include))
            fftw_ld_flags = spec['fftw'].libs.ld_flags
            options.append('FFT_LIBS={0}'.format(fftw_ld_flags))

        # External BLAS and LAPACK requires the correct link line into
        # BLAS_LIBS, do no use LAPACK_LIBS as the autoconf scripts indicate
        # that this variable is largely ignored/obsolete.

        # For many Spack packages, lapack.libs = blas.libs, hence it will
        # appear twice in in link line but this is harmless
        lapack_blas = spec['lapack'].libs + spec['blas'].libs

        # qe-6.5 fails to detect MKL for FFT if BLAS_LIBS is set due to
        # an unfortunate upsteam change in their autoconf/configure:
        # - qe-6.5/install/m4/x_ac_qe_blas.m4 only sets 'have_blas'
        #   but no 'have_mkl' if BLAS_LIBS is set (which seems to be o.k.)
        # - however, qe-6.5/install/m4/x_ac_qe_fft.m4 in 6.5 unfortunately
        #   relies on x_ac_qe_blas.m4 to detect MKL and set 'have_mkl'
        # - qe-5.4 up to 6.4.1 had a different logic and worked fine with
        #   BLAS_LIBS being set
        # However, MKL is correctly picked up by qe-6.5 for BLAS and FFT if
        # MKLROOT is set (which SPACK does automatically for ^mkl)
        if not ('quantum-espresso@6.5' in spec and '^mkl' in spec):
            options.append('BLAS_LIBS={0}'.format(lapack_blas.ld_flags))

        if '+scalapack' in spec:
            scalapack_option = 'intel' if '^mkl' in spec else 'yes'
            options.append('--with-scalapack={0}'.format(scalapack_option))

        if '+elpa' in spec:

            # Spec for elpa
            elpa = spec['elpa']

            # Compute the include directory from there: versions
            # of espresso prior to 6.1 requires -I in front of the directory
            elpa_include = '' if '@6.1:' in spec else '-I'
            elpa_include += join_path(
                elpa.headers.directories[0],
                'modules'
            )

            options.extend([
                '--with-elpa-include={0}'.format(elpa_include),
                '--with-elpa-lib={0}'.format(elpa.libs[0])
            ])

        if spec.variants['hdf5'].value != 'none':
            options.append('--with-hdf5={0}'.format(spec['hdf5'].prefix))
            if spec.satisfies('@6.4.1,6.5'):
                options.extend([
                    '--with-hdf5-include={0}'.format(
                        spec['hdf5'].headers.directories[0]
                    ),
                    '--with-hdf5-libs={0}'.format(
                        spec['hdf5:hl,fortran'].libs.ld_flags
                    )
                ])

        configure(*options)

        # Filter file must be applied after configure executes
        # QE 6.1.0 to QE 6.4 have `-L` missing in front of zlib library
        # This issue is backported through an internal patch in 6.4.1, but
        # can't be applied to the '+qmcpack' variant
        if spec.variants['hdf5'].value != 'none':
            if (spec.satisfies('@6.1.0:6.4.0') or
                (spec.satisfies('@6.4.1') and '+qmcpack' in spec)):
                make_inc = join_path(self.stage.source_path, 'make.inc')
                zlib_libs = spec['zlib'].prefix.lib + ' -lz'
                filter_file(
                    zlib_libs, format(spec['zlib'].libs.ld_flags), make_inc
                )

        if '+epw' in spec:
            make('all', 'epw')
        else:
            make('all')

        if 'platform=darwin' in spec:
            mkdirp(prefix.bin)
            install('bin/*.x', prefix.bin)
        else:
            make('install')
