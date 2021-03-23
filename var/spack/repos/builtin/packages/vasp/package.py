# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Vasp(MakefilePackage):
    """
    The Vienna Ab initio Simulation Package (VASP)
    is a computer program for atomic scale materials modelling,
    e.g. electronic structure calculations
    and quantum-mechanical molecular dynamics, from first principles.
    """

    homepage = "http://vasp.at"
    url      = "file://{0}/vasp.5.4.4.pl2.tgz".format(os.getcwd())
    manual_download = True

    version('6.1.1', sha256='e37a4dfad09d3ad0410833bcd55af6b599179a085299026992c2d8e319bf6927')
    version('5.4.4.pl2', sha256='98f75fd75399a23d76d060a6155f4416b340a1704f256a00146f89024035bc8e')
    version('5.4.4', sha256='5bd2449462386f01e575f9adf629c08cb03a13142806ffb6a71309ca4431cfb3')

    resource(name='vaspsol',
             git='https://github.com/henniggroup/VASPsol.git',
             tag='V1.0',
             when='+vaspsol')

    variant('scalapack', default=False,
            description='Enables build with SCALAPACK')

    variant('cuda', default=False,
            description='Enables running on Nvidia GPUs')

    variant('vaspsol', default=False,
            description='Enable VASPsol implicit solvation model\n'
            'https://github.com/henniggroup/VASPsol')

    depends_on('rsync', type='build')
    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw')
    depends_on('mpi', type=('build', 'link', 'run'))
    depends_on('netlib-scalapack', when='+scalapack')
    depends_on('cuda', when='+cuda')
    depends_on('qd', when='%nvhpc')

    conflicts('%gcc@:8', msg='GFortran before 9.x does not support all features needed to build VASP')
    conflicts('+vaspsol', when='+cuda', msg='+vaspsol only available for CPU')

    parallel = False

    def edit(self, spec, prefix):

        if '%gcc' in spec:
            make_include = join_path('arch', 'makefile.include.linux_gnu')
        elif '%nvhpc' in spec:
            make_include = join_path('arch', 'makefile.include.linux_pgi')
            filter_file('pgcc', spack_cc, make_include)
            filter_file('pgc++', spack_cxx, make_include, string=True)
            filter_file('pgfortran', spack_fc, make_include)
            filter_file('/opt/pgi/qd-2.3.17/install/include',
                        spec['qd'].prefix.include, make_include)
            filter_file('/opt/pgi/qd-2.3.17/install/lib',
                        spec['qd'].prefix.lib, make_include)
            filter_file('^SCALAPACK[ ]{0,}=.*$', 'SCALAPACK ?=', make_include)
        else:
            make_include = join_path('arch',
                                     'makefile.include.linux_' +
                                     spec.compiler.name)

        os.rename(make_include, 'makefile.include')

        # This bunch of 'filter_file()' is to make these options settable
        # as environment variables
        filter_file('^CPP_OPTIONS[ ]{0,}=[ ]{0,}',
                    'CPP_OPTIONS ?= ',
                    'makefile.include')
        filter_file('^FFLAGS[ ]{0,}=[ ]{0,}',
                    'FFLAGS ?= ',
                    'makefile.include')

        filter_file('^LIBDIR[ ]{0,}=.*$', '', 'makefile.include')
        filter_file('^BLAS[ ]{0,}=.*$', 'BLAS ?=', 'makefile.include')
        filter_file('^LAPACK[ ]{0,}=.*$', 'LAPACK ?=', 'makefile.include')
        filter_file('^FFTW[ ]{0,}?=.*$', 'FFTW ?=', 'makefile.include')
        filter_file('^MPI_INC[ ]{0,}=.*$', 'MPI_INC ?=', 'makefile.include')
        filter_file('-DscaLAPACK.*$\n', '', 'makefile.include')
        filter_file('^SCALAPACK*$', '', 'makefile.include')

        if '+cuda' in spec:
            filter_file('^OBJECTS_GPU[ ]{0,}=.*$',
                        'OBJECTS_GPU ?=',
                        'makefile.include')

            filter_file('^CPP_GPU[ ]{0,}=.*$',
                        'CPP_GPU ?=',
                        'makefile.include')

            filter_file('^CFLAGS[ ]{0,}=.*$',
                        'CFLAGS ?=',
                        'makefile.include')

        if '+vaspsol' in spec:
            copy('VASPsol/src/solvation.F', 'src/')

    def setup_build_environment(self, spack_env):
        spec = self.spec

        cpp_options = ['-DMPI -DMPI_BLOCK=8000',
                       '-Duse_collective', '-DCACHE_SIZE=4000',
                       '-Davoidalloc', '-Duse_bse_te',
                       '-Dtbdyn', '-Duse_shmem']
        if '%nvhpc' in self.spec:
            cpp_options.extend(['-DHOST=\\"LinuxPGI\\"', '-DPGI16',
                                '-Dqd_emulate'])
        else:
            cpp_options.append('-DHOST=\\"LinuxGNU\\"')
        if self.spec.satisfies('@6:'):
            cpp_options.append('-Dvasp6')

        cflags = ['-fPIC', '-DADD_']
        fflags = []
        if '%gcc' in spec or '%intel' in spec:
            fflags.append('-w')

        spack_env.set('BLAS', spec['blas'].libs.ld_flags)
        spack_env.set('LAPACK', spec['lapack'].libs.ld_flags)
        spack_env.set('FFTW', spec['fftw'].prefix)
        spack_env.set('MPI_INC', spec['mpi'].prefix.include)

        if '+scalapack' in spec:
            cpp_options.append('-DscaLAPACK')
            spack_env.set('SCALAPACK', spec['netlib-scalapack'].libs.ld_flags)

        if '+cuda' in spec:
            cpp_gpu = ['-DCUDA_GPU', '-DRPROMU_CPROJ_OVERLAP',
                       '-DCUFFT_MIN=28', '-DUSE_PINNED_MEMORY']

            objects_gpu = ['fftmpiw.o', 'fftmpi_map.o', 'fft3dlib.o',
                           'fftw3d_gpu.o', 'fftmpiw_gpu.o']

            cflags.extend(['-DGPUSHMEM=300', '-DHAVE_CUBLAS'])

            spack_env.set('CUDA_ROOT', spec['cuda'].prefix)
            spack_env.set('CPP_GPU', ' '.join(cpp_gpu))
            spack_env.set('OBJECTS_GPU', ' '.join(objects_gpu))

        if '+vaspsol' in spec:
            cpp_options.append('-Dsol_compat')

        if spec.satisfies('%gcc@10:'):
            fflags.append('-fallow-argument-mismatch')

        # Finally
        spack_env.set('CPP_OPTIONS', ' '.join(cpp_options))
        spack_env.set('CFLAGS', ' '.join(cflags))
        spack_env.set('FFLAGS', ' '.join(fflags))

    def build(self, spec, prefix):
        if '+cuda' in self.spec:
            make('gpu', 'gpu_ncl')
        else:
            make('std', 'gam', 'ncl')

    def install(self, spec, prefix):
        install_tree('bin/', prefix.bin)
