# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class QuantumEspresso(Package):
    """Quantum ESPRESSO is an integrated suite of Open-Source computer codes
    for electronic-structure calculations and materials modeling at the
    nanoscale. It is based on density-functional theory, plane waves, and
    pseudopotentials.
    """

    homepage = 'http://quantum-espresso.org'
    url = 'https://gitlab.com/QEF/q-e/-/archive/qe-6.6/q-e-qe-6.6.tar.gz'
    git = 'https://gitlab.com/QEF/q-e.git'

    maintainers = ['naromero77']

    version('develop', branch='develop')
    version('6.7', sha256='fe0ce74ff736b10d2a20c9d59025c01f88f86b00d229c123b1791f1edd7b4315',
            url='https://gitlab.com/QEF/q-e/-/archive/qe-6.7MaX-Release/q-e-qe-6.7MaX-Release.tar.gz'
            )
    version('6.6', sha256='924656cb083f52e5d2fe71ade05881389dac64b45316f1bdd6dee1c6170a672c')
    version('6.5', sha256='258b2a8a6280e86dad779e5c56356d8b35dc96d12ff33dabeee914bc03d6d602')
    version('6.4.1', sha256='b0d7e9f617b848753ad923d8c6ca5490d5d82495f82b032b71a0ff2f2e9cfa08')
    version('6.4', sha256='781366d03da75516fdcf9100a1caadb26ccdd1dedd942a6f8595ff0edca74bfe')
    version('6.3',   sha256='4067c8fffa957aabbd5cf2439e2fcb6cf3752325393c67a17d99fd09edf8689c')
    version('6.2.1', sha256='11fe24b4a9d85834f8b6d429baebed8b360a685ecfae222887ed451e118a9156')
    version('6.2.0', sha256='e204df367c8ea1a50c7534b44481841d835a542a23ae71c3e33ad712fc636c8b')
    version('6.1.0', sha256='fd2c2eb346b3ca8f08138df5ef3f69b466c256d2119db40eea1b578b0a42c66e')
    version('6.0.0', sha256='bc77d9553bf5a9253ae74058dffb1d6e5fb61093188e78d3b8d8564755136f19')
    version('5.4',   sha256='e3993fccae9cea04a5c6492e8b961a053a63727051cb5c4eb6008f62cda8f335')
    version('5.3',   sha256='3b26038efb9e3f8ac7a2b950c31d8c29169a3556c0b68c299eb88a4be8dc9048')

    resource(name='environ',
             git='https://github.com/environ-developers/Environ.git',
             tag='v1.1',
             when='@6.3:6.4.99 +environ',
             destination='.'
             )

    resource(name='environ',
             git='https://github.com/environ-developers/Environ.git',
             tag='v1.0',
             when='@6.2.1:6.2.99 +environ',
             destination='.'
             )

    variant('mpi', default=True, description='Builds with mpi support')
    variant('openmp', default=False, description='Enables openMP support')
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
    desc = desc + 'to False for third party patches or plugins'
    variant('patch', default=True, description=desc)

    # QMCPACK converter patch
    # https://github.com/QMCPACK/qmcpack/tree/develop/external_codes/quantum_espresso
    variant('qmcpack', default=False,
            description='Build QE-to-QMCPACK wave function converter')

    variant('environ', default=False,
            description='Enables support for introducing environment effects '
            'into atomistic first-principles simulations.'
            'See http://quantum-environ.org/about.html')

    # Dependencies
    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw-api@3')
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

    # PATCHES SECTION
    # THIRD-PARTY PATCHES
    # NOTE: *SOME* third-party patches will require deactivation of
    # upstream patches using `~patch` variant

    # QMCPACK converter patches for QE 6.4.1, 6.4, and 6.3
    conflicts('@:6.2,6.5:', when='+qmcpack',
              msg='QMCPACK converter NOT available for this version of QE')

    # Internal compiler error gcc8 and a64fx, I check only 6.5 and 6.6
    conflicts('@5.3:', when='%gcc@8 target=a64fx',
              msg='Internal compiler error with gcc8 and a64fx')

    conflicts('@6.5:', when='+environ',
              msg='6.4.x is the latest QE series supported by Environ')

    # 6.4.1
    patch_url = 'https://raw.githubusercontent.com/QMCPACK/qmcpack/develop/external_codes/quantum_espresso/add_pw2qmcpack_to_qe-6.4.1.diff'
    patch_checksum = '57cb1b06ee2653a87c3acc0dd4f09032fcf6ce6b8cbb9677ae9ceeb6a78f85e2'
    patch(patch_url, sha256=patch_checksum, when='@6.4.1+qmcpack')
    # 6.4
    patch_url = 'https://raw.githubusercontent.com/QMCPACK/qmcpack/develop/external_codes/quantum_espresso/add_pw2qmcpack_to_qe-6.4.diff'
    patch_checksum = 'ef08f5089951be902f0854a4dbddaa7b01f08924cdb27decfade6bef0e2b8994'
    patch(patch_url, sha256=patch_checksum, when='@6.4:6.4.0+qmcpack')
    # 6.3
    patch_url = 'https://raw.githubusercontent.com/QMCPACK/qmcpack/develop/external_codes/quantum_espresso/add_pw2qmcpack_to_qe-6.3.diff'
    patch_checksum = '2ee346e24926479f5e96f8dc47812173a8847a58354bbc32cf2114af7a521c13'
    patch(patch_url, sha256=patch_checksum, when='@6.3+qmcpack')

    # ELPA
    patch('dspev_drv_elpa.patch', when='@6.1.0:+elpa ^elpa@2016.05.004')
    patch('dspev_drv_elpa.patch', when='@6.1.0:+elpa ^elpa@2016.05.003')

    # QE UPSTREAM PATCHES
    # QE 6.6 fix conpile error when FFT_LIBS is specified.
    patch('https://gitlab.com/QEF/q-e/-/commit/cf1fedefc20d39f5cd7551ded700ea4c77ad6e8f.diff',
          sha256='8f179663a8d031aff9b1820a32449942281195b6e7b1ceaab1f729651b43fa58',
          when='+patch@6.6')
    # QE 6.5 INTENT(OUT) without settig value in tetra_weights_only(..., ef):
    # For Fujitsu compiler
    patch('https://gitlab.com/QEF/q-e/-/commit/8f096b53e75026701c681c508e2c24a9378c0950.diff',
          sha256='f4f1cce4182b57ac797c8f6ec8460fe375ee96385fcd8f6a61e1460bc957eb67',
          when='+patch@6.5')
    # QE 6.5 Fix INTENT
    # For Fujitsu compiler
    patch('https://gitlab.com/QEF/q-e/-/commit/c2a86201ed72693ffa50cc99b22f5d3365ae2c2b.diff',
          sha256='b2dadc0bc008a3ad4b74ae85cc380dd2b63f2ae43a634e6f9d8db8077efcea6c',
          when='+patch@6.5')
    # QE 6.3 requires multiple patches to fix MKL detection
    # There may still be problems on Mac with MKL detection
    patch('https://gitlab.com/QEF/q-e/commit/0796e1b7c55c9361ecb6515a0979280e78865e36.diff',
          sha256='bc8c5b8523156cee002d97dab42a5976dffae20605da485a427b902a236d7e6b',
          when='+patch@6.3:6.3.0')

    # QE 6.3 `make install` broken and a patch must be applied
    patch('https://gitlab.com/QEF/q-e/commit/88e6558646dbbcfcafa5f3fa758217f6062ab91c.diff',
          sha256='b776890d008e16cca28c31299c62f47de0ba606b900b17cbc27c041f45e564ca',
          when='+patch@6.3:6.3.0')

    # QE 6.4.1 patch to work around configure issues that only appear in the
    # Spack environment. We now are able to support:
    # `spack install qe~mpi~scalapack hdf5=serial`
    patch('https://gitlab.com/QEF/q-e/commit/5fb1195b0844e1052b7601f18ab5c700f9cbe648.diff',
          sha256='b1aa3179ee1c069964fb9c21f3b832aebeae54947ce8d3cc1a74e7b154c3c10f',
          when='+patch@6.4.1:6.5.0')

    # QE 6.4.1 Fix intent for Fujitsu compiler
    patch('fj-intent.6.4.1.patch', when='+patch@6.4.1')
    # QE 6.4.1 Fix intent
    patch('https://gitlab.com/QEF/q-e/-/commit/c2a86201ed72693ffa50cc99b22f5d3365ae2c2b.diff',
          sha256='b2dadc0bc008a3ad4b74ae85cc380dd2b63f2ae43a634e6f9d8db8077efcea6c',
          when='+patch@6.4.1')

    # QE 6.4.1 Small fixes for XLF compilation
    patch('https://gitlab.com/QEF/q-e/-/commit/cf088926d68792cbaea48960c222e336a3965df6.diff',
          sha256='bbceba1fb08d01d548d4393bbcaeae966def13f75884268a0f84448457b8eaa3',
          when='+patch@6.4.1:6.5.0')

    # Configure updated to work with NVIDIA compilers
    patch('nvhpc.patch', when='@6.5 %nvhpc')

    # Configure updated to work with Fujitsu compilers
    patch('fj.6.5.patch', when='@6.5+patch %fj')
    patch('fj.6.6.patch', when='@6.6:6.7+patch %fj')

    # extlibs_makefile updated to work with fujitsu compilers
    patch('fj-fox.patch', when='+patch %fj')

    # Spurious problems running in parallel the Makefile
    # generated by the configure
    parallel = False

    def install(self, spec, prefix):

        prefix_path = prefix.bin if '@:5.4.0' in spec else prefix
        options = ['-prefix={0}'.format(prefix_path)]

        # This additional flag is needed anytime the target architecture
        # does not match the host architecture, which results in a binary that
        # configure cannot execute on the login node. This is how we detect
        # cross compilation: If the platform is NOT either Linux or Darwin
        # and the target=backend, that we are in the cross-compile scenario
        # scenario. This should cover Cray, BG/Q, and other custom platforms.
        # The other option is to list out all the platform where you would be
        # cross compiling explicitly.
        if not (spec.satisfies('platform=linux') or
                spec.satisfies('platform=darwin')):
            if spec.satisfies('target=backend'):
                options.append('--host')

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
            options.append('CC={0}'.format(env['SPACK_CC']))

        options.append('F77={0}'.format(env['SPACK_F77']))
        options.append('F90={0}'.format(env['SPACK_FC']))

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
            if '^mkl' in spec:
                if '^openmpi' in spec:
                    scalapack_option = 'yes'
                else:  # mpich, intel-mpi
                    scalapack_option = 'intel'
            else:
                scalapack_option = 'yes'
            options.append('--with-scalapack={0}'.format(scalapack_option))
            scalapack_lib = spec['scalapack'].libs
            options.append('SCALAPACK_LIBS={0}'.format(scalapack_lib.ld_flags))

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

        if '+environ' in spec:
            addsonpatch = Executable('./install/addsonpatch.sh')
            environpatch = Executable('./Environ/patches/environpatch.sh')
            makedeps = Executable('./install/makedeps.sh')

            addsonpatch('Environ', 'Environ/src', 'Modules', '-patch')

            environpatch('-patch')

            makedeps()

            make('pw')

        if 'platform=darwin' in spec:
            mkdirp(prefix.bin)
            install('bin/*.x', prefix.bin)
        else:
            make('install')
