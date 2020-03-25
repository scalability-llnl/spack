# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import os.path
import copy

import spack.util.environment


class Cp2k(MakefilePackage, CudaPackage):
    """CP2K is a quantum chemistry and solid state physics software package
    that can perform atomistic simulations of solid state, liquid, molecular,
    periodic, material, crystal, and biological systems
    """
    homepage = 'https://www.cp2k.org'
    url = 'https://github.com/cp2k/cp2k/releases/download/v3.0.0/cp2k-3.0.tar.bz2'
    git = 'https://github.com/cp2k/cp2k.git'
    list_url = 'https://github.com/cp2k/cp2k/releases'

    version('6.1', sha256='af803558e0a6b9e9d9ce8a3ab955ba32bacd179922455424e061c82c9fefa34b')
    version('5.1', sha256='e23613b593354fa82e0b8410e17d94c607a0b8c6d9b5d843528403ab09904412')
    version('4.1', sha256='4a3e4a101d8a35ebd80a9e9ecb02697fb8256364f1eccdbe4e5a85d31fe21343')
    version('3.0', sha256='1acfacef643141045b7cbade7006f9b7538476d861eeecd9658c9e468dc61151')
    version('develop', branch='master', submodules="True")

    variant('mpi', default=True, description='Enable MPI support')
    variant('blas', default='openblas', values=('openblas', 'mkl', 'accelerate'),
            description='Enable the use of OpenBlas/MKL/Accelerate')
    variant('openmp', default=False, description='Enable OpenMP support')
    variant('smm', default='libxsmm', values=('libxsmm', 'libsmm', 'blas'),
            description='Library for small matrix multiplications')
    variant('plumed', default=False, description='Enable PLUMED support')
    variant('libxc', default=True,
            description='Support additional functionals via libxc')
    variant('pexsi', default=False,
            description=('Enable the alternative PEXSI method'
                         'for density matrix evaluation'))
    variant('elpa', default=False,
            description='Enable optimised diagonalisation routines from ELPA')
    variant('sirius', default=False,
            description=('Enable planewave electronic structure'
                         ' calculations via SIRIUS'))

    # override cuda_arch from CudaPackage since we only support one arch
    # at a time and only specific ones for which we have parameter files
    # for optimal kernels
    variant('cuda_arch',
            description='CUDA architecture',
            default='none',
            values=('none', '35', '37', '60', '70'),
            multi=False)
    variant('cuda_arch_35_k20x', default=False,
            description=('CP2K (resp. DBCSR) has specific parameter sets for'
                         ' different GPU models. Enable this when building'
                         ' with cuda_arch=35 for a K20x instead of a K40'))
    variant('cuda_fft', default=False,
            description=('Use CUDA also for FFTs in the PW part of CP2K'))
    variant('cuda_blas', default=False,
            description=('Use CUBLAS for general matrix operations in DBCSR'))

    HFX_LMAX_RANGE = range(4, 8)

    variant('lmax',
            description='Maximum supported angular momentum (HFX and others)',
            default='5',
            values=list(HFX_LMAX_RANGE),
            multi=False)

    depends_on('python', type='build')

    depends_on('fftw@3:', when='~openmp')
    depends_on('fftw@3:+openmp', when='+openmp')

    # see #1712 for the reason to enumerate BLAS libraries here
    depends_on('openblas threads=none', when='blas=openblas ~openmp')
    depends_on('openblas threads=openmp', when='blas=openblas +openmp')
    depends_on('lapack', when='blas=openblas ~openmp')

    depends_on('mkl', when="blas=mkl")

    conflicts('blas=accelerate', '+openmp')  # there is no Accelerate with OpenMP support

    # require libxsmm-1.11+ since 1.10 can leak file descriptors in Fortran
    depends_on('libxsmm@1.11:~header-only', when='smm=libxsmm')
    # use pkg-config (support added in libxsmm-1.10) to link to libxsmm
    depends_on('pkgconfig', type='build', when='smm=libxsmm')
    # ... and in CP2K 7.0+ for linking to libint2
    depends_on('pkgconfig', type='build', when='@7.0:')

    # libint & libxc are always statically linked
    depends_on('libint@1.1.4:1.2', when='@3.0:6.9', type='build')
    for lmax in HFX_LMAX_RANGE:
        # libint2 can be linked dynamically again
        depends_on('libint@2.6.0:+fortran tune=cp2k-lmax-{0}'.format(lmax),
                   when='@7.0: lmax={0}'.format(lmax))

    depends_on('libxc@2.2.2:', when='+libxc@:5.5999', type='build')
    depends_on('libxc@4.0.3:', when='+libxc@6.0:6.9', type='build')
    depends_on('libxc@4.0.3:', when='+libxc@7.0:')

    depends_on('mpi@2:', when='+mpi')
    depends_on('scalapack', when='+mpi')
    depends_on('elpa@2011.12:2016.13+openmp', when='+openmp+elpa@:5.999')
    depends_on('elpa@2011.12:2017.11+openmp', when='+openmp+elpa@6.0:')
    depends_on('elpa@2011.12:2016.13~openmp', when='~openmp+elpa@:5.999')
    depends_on('elpa@2011.12:2017.11~openmp', when='~openmp+elpa@6.0:')
    depends_on('plumed+shared+mpi', when='+plumed+mpi')
    depends_on('plumed+shared~mpi', when='+plumed~mpi')

    # while we link statically against PEXSI, its own deps may be linked in
    # dynamically, therefore can't set this as pure build-type dependency.
    depends_on('pexsi+fortran@0.9.0:0.9.999', when='+pexsi@:4.999')
    depends_on('pexsi+fortran@0.10.0:', when='+pexsi@5.0:')

    # only OpenMP should be consistenly used, all other common things
    # like ELPA, SCALAPACK are independent and Spack will ensure that
    # a consistent/compat. combination is pulled in to the dependency graph.
    depends_on('sirius+fortran+vdwxc+shared+openmp', when='+sirius+openmp')
    depends_on('sirius+fortran+vdwxc+shared~openmp', when='+sirius~openmp')

    # the bundled libcusmm uses numpy in the parameter prediction (v7+)
    depends_on('py-numpy', when='@7:+cuda', type='build')

    # PEXSI, ELPA and SIRIUS need MPI in CP2K
    conflicts('~mpi', '+pexsi')
    conflicts('~mpi', '+elpa')
    conflicts('~mpi', '+sirius')
    conflicts('+sirius', '@:6.999')  # sirius support was introduced in 7+

    conflicts('~cuda', '+cuda_fft')
    conflicts('~cuda', '+cuda_blas')

    # Apparently cp2k@4.1 needs an "experimental" version of libwannier.a
    # which is only available contacting the developer directly. See INSTALL
    # in the stage of cp2k@4.1
    depends_on('wannier90', when='@3.0+mpi', type='build')

    # CP2K needs compiler specific compilation flags, e.g. optflags
    conflicts('%clang')
    conflicts('%cray')
    conflicts('%nag')
    conflicts('%xl')

    @property
    def makefile_architecture(self):
        return '{0.architecture}-{0.compiler.name}'.format(self.spec)

    @property
    def makefile_version(self):
        return '{prefix}{suffix}'.format(
            prefix='p' if '+mpi' in self.spec else 's',
            suffix='smp' if '+openmp' in self.spec else 'opt'
        )

    @property
    def makefile(self):
        makefile_basename = '.'.join([
            self.makefile_architecture, self.makefile_version
        ])
        return os.path.join('arch', makefile_basename)

    @property
    def archive_files(self):
        return [os.path.join(self.stage.source_path, self.makefile)]

    def edit(self, spec, prefix):

        fftw = spec['fftw:openmp' if '+openmp' in spec else 'fftw']

        optimization_flags = {
            'gcc': [
                '-O2',
                '-funroll-loops',
                '-ftree-vectorize',
            ],
            'intel': ['-O2', '-pc64', '-unroll'],
            'pgi': ['-fast'],
        }

        dflags = ['-DNDEBUG']
        cppflags = [
            '-D__LIBINT',
            '-D__FFTW3',
            fftw.headers.cpp_flags,
        ]

        if '@:6.9' in spec:
            cppflags += [
                '-D__LIBINT_MAX_AM=6',
                '-D__LIBDERIV_MAX_AM1=5',
            ]

        if '^mpi@3:' in spec:
            cppflags.append('-D__MPI_VERSION=3')
        elif '^mpi@2:' in spec:
            cppflags.append('-D__MPI_VERSION=2')

        cflags = optimization_flags[self.spec.compiler.name][:]
        cxxflags = optimization_flags[self.spec.compiler.name][:]
        fcflags = optimization_flags[self.spec.compiler.name][:]
        nvflags = ['-O3']
        ldflags = []
        libs = []
        gpuver = ''

        if '%intel' in spec:
            cflags.append('-fp-model precise')
            cxxflags.append('-fp-model precise')
            fcflags += [
                '-fp-model source',
                '-heap-arrays 64',
                '-g',
                '-traceback',
            ]
        elif '%gcc' in spec:
            fcflags.extend([
                '-ffree-form',
                '-ffree-line-length-none',
                '-ggdb',  # make sure we get proper Fortran backtraces
            ])
        elif '%pgi' in spec:
            fcflags.extend(['-Mfreeform', '-Mextend'])

        if '+openmp' in spec:
            cflags.append(self.compiler.openmp_flag)
            cxxflags.append(self.compiler.openmp_flag)
            fcflags.append(self.compiler.openmp_flag)
            ldflags.append(self.compiler.openmp_flag)
            nvflags.append('-Xcompiler="{0}"'.format(
                self.compiler.openmp_flag))

        ldflags.append(fftw.libs.search_flags)

        if 'superlu-dist@4.3' in spec:
            ldflags.insert(0, '-Wl,--allow-multiple-definition')

        if '@:6.9' in spec:
            # libint-1.x.y has to be linked statically to work around
            # inconsistencies in its Fortran interface definition
            # (short-int vs int) which otherwise causes segfaults at runtime
            # due to wrong offsets into the shared library symbols.
            libs.extend([
                os.path.join(spec['libint'].libs.directories[0], 'libderiv.a'),
                os.path.join(spec['libint'].libs.directories[0], 'libint.a'),
            ])
        else:
            fcflags += ['$(shell pkg-config --cflags libint2)']
            libs += ['$(shell pkg-config --libs libint2)']

        if '+plumed' in self.spec:
            dflags.extend(['-D__PLUMED2'])
            cppflags.extend(['-D__PLUMED2'])
            libs.extend([
                os.path.join(self.spec['plumed'].prefix.lib,
                             'libplumed.{0}'.format(dso_suffix))
            ])

        fc = self.compiler.fc if '~mpi' in spec else self.spec['mpi'].mpifc

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

        # FFTW, LAPACK, BLAS
        lapack = spec['lapack'].libs
        blas = spec['blas'].libs
        ldflags.append((lapack + blas).search_flags)
        libs.extend([str(x) for x in (fftw.libs, lapack, blas)])

        if self.spec.variants['blas'].value == 'mkl':
            cppflags += ['-D__MKL']
        elif self.spec.variants['blas'].value == 'accelerate':
            cppflags += ['-D__ACCELERATE']

        # MPI
        if '+mpi' in self.spec:
            cppflags.extend([
                '-D__parallel',
                '-D__SCALAPACK'
            ])

            scalapack = spec['scalapack'].libs
            ldflags.append(scalapack.search_flags)

            libs.extend(scalapack)
            libs.extend(self.spec['mpi:cxx'].libs)
            libs.extend(self.compiler.stdcxx_libs)

            if 'wannier90' in spec:
                cppflags.append('-D__WANNIER90')
                wannier = os.path.join(
                    spec['wannier90'].libs.directories[0], 'libwannier.a'
                )
                libs.append(wannier)

        if '+libxc' in spec:
            cppflags += ['-D__LIBXC']

            if '@:6.9' in spec:
                libxc = spec['libxc:fortran,static']
                cppflags += [libxc.headers.cpp_flags]
                ldflags.append(libxc.libs.search_flags)
                libs.append(str(libxc.libs))
            else:
                fcflags += ['$(shell pkg-config --cflags libxcf03)']
                libs += ['$(shell pkg-config --libs libxcf03)']

        if '+pexsi' in self.spec:
            cppflags.append('-D__LIBPEXSI')
            fcflags.append('-I' + os.path.join(
                spec['pexsi'].prefix, 'fortran'))
            libs.extend([
                os.path.join(spec['pexsi'].libs.directories[0],
                             'libpexsi.a'),
                os.path.join(spec['superlu-dist'].libs.directories[0],
                             'libsuperlu_dist.a'),
                os.path.join(
                    spec['parmetis'].libs.directories[0],
                    'libparmetis.{0}'.format(dso_suffix)
                ),
                os.path.join(
                    spec['metis'].libs.directories[0],
                    'libmetis.{0}'.format(dso_suffix)
                ),
            ])

        if '+elpa' in self.spec:
            elpa = spec['elpa']
            elpa_suffix = '_openmp' if '+openmp' in elpa else ''
            elpa_incdir = elpa.headers.directories[0]

            fcflags += ['-I{0}'.format(os.path.join(elpa_incdir, 'modules'))]
            libs.append(os.path.join(elpa.libs.directories[0],
                                     ('libelpa{elpa_suffix}.{dso_suffix}'
                                      .format(elpa_suffix=elpa_suffix,
                                              dso_suffix=dso_suffix))))

            if spec.satisfies('@:4.999'):
                if elpa.satisfies('@:2014.5.999'):
                    cppflags.append('-D__ELPA')
                elif elpa.satisfies('@2014.6:2015.10.999'):
                    cppflags.append('-D__ELPA2')
                else:
                    cppflags.append('-D__ELPA3')
            else:
                cppflags.append('-D__ELPA={0}{1:02d}'
                                .format(elpa.version[0],
                                        int(elpa.version[1])))
                fcflags += ['-I{0}'.format(os.path.join(elpa_incdir, 'elpa'))]

        if self.spec.satisfies('+sirius'):
            sirius = spec['sirius']
            cppflags.append('-D__SIRIUS')
            fcflags += ['-I{0}'.format(os.path.join(sirius.prefix, 'fortran'))]
            libs += list(sirius.libs)

        if self.spec.satisfies('+cuda'):
            cppflags += ['-D__ACC']
            libs += ['-lcudart', '-lnvrtc', '-lcuda']

            if self.spec.satisfies('+cuda_blas'):
                cppflags += ['-D__DBCSR_ACC=2']
                libs += ['-lcublas']
            else:
                cppflags += ['-D__DBCSR_ACC']

            if self.spec.satisfies('+cuda_fft'):
                cppflags += ['-D__PW_CUDA']
                libs += ['-lcufft', '-lcublas']

            cuda_arch = self.spec.variants['cuda_arch'].value
            if cuda_arch:
                gpuver = {
                    '35': 'K40',
                    '37': 'K80',
                    '60': 'P100',
                    '70': 'V100',
                }[cuda_arch]

                if (cuda_arch == '35'
                        and self.spec.satisfies('+cuda_arch_35_k20x')):
                    gpuver = 'K20X'

        if 'smm=libsmm' in spec:
            lib_dir = os.path.join(
                'lib', self.makefile_architecture, self.makefile_version
            )
            mkdirp(lib_dir)
            try:
                copy(env['LIBSMM_PATH'], os.path.join(lib_dir, 'libsmm.a'))
            except KeyError:
                raise KeyError('Point environment variable LIBSMM_PATH to '
                               'the absolute path of the libsmm.a file')
            except IOError:
                raise IOError('The file LIBSMM_PATH pointed to does not '
                              'exist. Note that it must be absolute path.')
            cppflags.extend([
                '-D__HAS_smm_dnn',
                '-D__HAS_smm_vec',
            ])
            libs.append('-lsmm')

        elif 'smm=libxsmm' in spec:
            cppflags.extend([
                '-D__LIBXSMM',
                '$(shell pkg-config --cflags-only-other libxsmmf)',
            ])
            fcflags.append('$(shell pkg-config --cflags-only-I libxsmmf)')
            libs.append('$(shell pkg-config --libs libxsmmf)')

        dflags.extend(cppflags)
        cflags.extend(cppflags)
        cxxflags.extend(cppflags)
        fcflags.extend(cppflags)
        nvflags.extend(cppflags)

        with open(self.makefile, 'w') as mkf:
            if '+plumed' in self.spec:
                # Include Plumed.inc in the Makefile
                mkf.write('include {0}\n'.format(
                    self.spec['plumed'].package.plumed_inc
                ))

            mkf.write('CC = {0.compiler.cc}\n'.format(self))
            if '%intel' in self.spec:
                intel_bin_dir = ancestor(self.compiler.cc)
                # CPP is a commented command in Intel arch of CP2K
                # This is the hack through which cp2k developers avoid doing :
                #
                # ${CPP} <file>.F > <file>.f90
                #
                # and use `-fpp` instead
                mkf.write('CPP = # {0.compiler.cc} -P\n\n'.format(self))
                mkf.write('AR = {0}/xiar -r\n\n'.format(intel_bin_dir))
            else:
                mkf.write('CPP = # {0.compiler.cc} -E\n\n'.format(self))
                mkf.write('AR = ar -r\n\n')
            mkf.write('FC = {0}\n'.format(fc))
            mkf.write('LD = {0}\n'.format(fc))

            if self.spec.satisfies('+cuda'):
                mkf.write('NVCC = {0}\n'.format(
                    os.path.join(self.spec['cuda'].prefix, 'bin', 'nvcc')))

            # Write compiler flags to file
            mkf.write('DFLAGS = {0}\n\n'.format(' '.join(dflags)))
            mkf.write('CPPFLAGS = {0}\n\n'.format(' '.join(cppflags)))
            mkf.write('CFLAGS = {0}\n\n'.format(' '.join(cflags)))
            mkf.write('CXXFLAGS = {0}\n\n'.format(' '.join(cxxflags)))
            mkf.write('NVFLAGS = {0}\n\n'.format(' '.join(nvflags)))
            mkf.write('FCFLAGS = {0}\n\n'.format(' '.join(fcflags)))
            mkf.write('LDFLAGS = {0}\n\n'.format(' '.join(ldflags)))
            if '%intel' in spec:
                mkf.write('LDFLAGS_C = {0}\n\n'.format(
                    ' '.join(ldflags) + ' -nofor_main')
                )
            mkf.write('LIBS = {0}\n\n'.format(' '.join(libs)))
            mkf.write('GPUVER = {0}\n\n'.format(gpuver))
            mkf.write('DATA_DIR = {0}\n\n'.format(self.prefix.share.data))

    @property
    def build_directory(self):
        build_dir = self.stage.source_path

        if self.spec.satisfies('@:6.9999'):
            # prior to version 7.1 was the Makefile located in makefiles/
            build_dir = os.path.join(build_dir, 'makefiles')

        return build_dir

    @property
    def build_targets(self):
        return [
            'ARCH={0}'.format(self.makefile_architecture),
            'VERSION={0}'.format(self.makefile_version)
        ]

    def build(self, spec, prefix):
        # Apparently the Makefile bases its paths on PWD
        # so we need to set PWD = self.build_directory
        with spack.util.environment.set_env(PWD=self.build_directory):
            super(Cp2k, self).build(spec, prefix)

    def install(self, spec, prefix):
        exe_dir = os.path.join('exe', self.makefile_architecture)
        install_tree(exe_dir, self.prefix.bin)
        install_tree('data', self.prefix.share.data)

    def check(self):
        data_dir = os.path.join(self.stage.source_path, 'data')

        # CP2K < 7 still uses $PWD to detect the current working dir
        # and Makefile is in a subdir, account for both facts here:
        with spack.util.environment.set_env(CP2K_DATA_DIR=data_dir,
                                            PWD=self.build_directory):
            with working_dir(self.build_directory):
                make('test', *self.build_targets)
