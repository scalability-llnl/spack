# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.compiler import UnsupportedCompilerFlag
from spack.package import *


class Warpx(MakefilePackage):
    """WarpX is an advanced electromagnetic Particle-In-Cell code. It supports
    many features including Perfectly-Matched Layers (PML) and mesh refinement.
    In addition, WarpX is a highly-parallel and highly-optimized code and
    features hybrid OpenMP/MPI parallelization, advanced vectorization
    techniques and load balancing capabilities.
    """

    homepage = "https://ecp-warpx.github.io/index.html"
    git      = "https://github.com/ECP-WarpX/WarpX.git"

    maintainers = ['ax3l', 'dpgrote', 'MaxThevenet', 'RemiLehe']

    version('develop', tag='development')

    variant('dims',
            default='3',
            values=('2', '3', 'rz'),
            multi=False,
            description='Number of spatial dimensions')
    variant('backend',
            default='openmp',
            values=('openmp', 'cuda', 'hip'),
            multi=True,
            description='Programming model for compute kernels')
    variant('mpi', default=True, description='Enable MPI support')
    variant('psatd', default=True, description='Enable PSATD solver support')
    variant('debug', default=False, description='Enable debugging features')
    variant('tprof', default=True, description='Enable tiny profiling features')
    variant('openpmd', default=True, description='Enable openPMD I/O')
    variant('ascent', default=False, description='Enable Ascent in situ vis')

    depends_on('cuda@9.2.88:', when='backend=cuda')
    depends_on('mpi', when='+mpi')
    depends_on('fftw@3:', when='+psatd backend=openmp')
    depends_on('fftw +mpi', when='+psatd +mpi backend=openmp')
    depends_on('blaspp', when='+psatd dims=rz')
    depends_on('lapackpp', when='+psatd dims=rz')
    depends_on('pkgconfig', type='build', when='+openpmd')
    depends_on('python', type='build')  # AMReX' build system info
    depends_on('openpmd-api@0.12.0:,dev', when='+openpmd')
    depends_on('openpmd-api +mpi', when='+openpmd +mpi')
    depends_on('ascent', when='+ascent')
    depends_on('ascent +cuda', when='+ascent backend=cuda')
    depends_on('ascent +mpi', when='+ascent +mpi')

    resource(name='amrex',
             git='https://github.com/AMReX-Codes/amrex.git',
             when='@develop',
             tag='development')

    resource(name='picsar',
             git='https://bitbucket.org/berkeleylab/picsar.git',
             tag='master')

    conflicts('backend=cuda', when='backend=hip',
              msg='WarpX can be compiled with either CUDA or HIP backend')
    conflicts('backend=hip', msg='WarpX\' HIP backend is not yet implemented')

    def edit(self, spec, prefix):
        comp = 'gcc'
        vendors = {'%gcc': 'gcc', '%intel': 'intel',
                   '%apple-clang': 'llvm', '%clang': 'llvm'}
        for key, value in vendors.items():
            if self.spec.satisfies(key):
                comp = value

        # Returns the string TRUE or FALSE
        torf = lambda s: repr(s in spec).upper()

        try:
            self.compiler.openmp_flag
        except UnsupportedCompilerFlag:
            use_omp = 'FALSE'
        else:
            use_omp = torf('backend=openmp')

        makefile = FileFilter('GNUmakefile')
        makefile.filter('AMREX_HOME .*', 'AMREX_HOME = amrex')
        makefile.filter('PICSAR_HOME .*', 'PICSAR_HOME = picsar')
        makefile.filter('COMP .*', 'COMP = {0}'.format(comp))
        makefile.filter('USE_MPI .*',
                        'USE_MPI = {0}'.format(torf('+mpi')))
        if 'dims=rz' in spec:
            makefile.filter('USE_RZ .*', 'USE_RZ = TRUE')
        else:
            makefile.filter('DIM .*', 'DIM = {0}'.format(
                int(spec.variants['dims'].value)))
        makefile.filter('USE_PSATD .*',
                        'USE_PSATD = {0}'.format(torf('+psatd')))
        makefile.filter('USE_OMP .*',
                        'USE_OMP = {0}'.format(use_omp))
        makefile.filter('USE_GPU .*',
                        'USE_GPU = {0}'.format(torf('backend=cuda')))
        makefile.filter('USE_HIP .*',
                        'USE_HIP = {0}'.format(torf('backend=hip')))
        makefile.filter('USE_OPENPMD .*',
                        'USE_OPENPMD = {0}'.format(torf('+openpmd')))
        makefile.filter('USE_ASCENT_INSITU .*',
                        'USE_ASCENT_INSITU = {0}'.format(torf('+ascent')))
        makefile.filter('DEBUG .*',
                        'DEBUG = {0}'.format(torf('+debug')))
        makefile.filter('TINY_PROFILE .*',
                        'TINY_PROFILE = {0}'.format(torf('+tprof')))
        makefile.filter('EBASE .*', 'EBASE = warpx')

    def setup_build_environment(self, env):
        # --- Fool the compiler into using the "unknown" configuration.
        # --- With this, it will use the spack provided mpi.
        env.set('HOSTNAME', 'unknown')
        env.set('NERSC_HOST', 'unknown')

    def install(self, spec, prefix):
        make('WarpxBinDir = {0}'.format(prefix.bin), 'all')
