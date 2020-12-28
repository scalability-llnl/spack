# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Relion(CMakePackage, CudaPackage):
    """RELION (for REgularised LIkelihood OptimisatioN, pronounce rely-on) is a
    stand-alone computer program that employs an empirical Bayesian approach to
    refinement of (multiple) 3D reconstructions or 2D class averages in
    electron cryo-microscopy (cryo-EM)."""

    homepage = "http://http://www2.mrc-lmb.cam.ac.uk/relion"
    git      = "https://github.com/3dem/relion.git"

    # 3.1 is beta but referenced in published papers
    # prefer stable 3.0 until no longer beta
    version('3.1_beta', branch='ver3.1')

    # 3.0.8 latest release in 3.0 branch
    # prefer for now
    version('3.0.8', tag='3.0.8', preferred=True)
    version('3.0.7', tag='3.0.7')

    # relion master contains development code
    # contains 3.0 branch code
    version('master')

    variant('gui', default=True, description="build the gui")
    variant('cuda', default=True, description="enable compute on gpu")
    variant('double', default=True, description="double precision (cpu) code")
    variant('double-gpu', default=False, description="double precision gpu")
    # if built with purpose=cluster then relion will link to gpfs libraries
    # if that's not desirable then use purpose=desktop
    variant('purpose', default='cluster', values=('cluster', 'desktop'),
            description="build relion for use in cluster or desktop")
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo',
                    'Profiling', 'Benchmarking'))

    depends_on('mpi')
    depends_on('cmake@3:', type='build')
    depends_on('fftw precision=float,double')
    depends_on('fltk', when='+gui')
    depends_on('libtiff')

    depends_on('cuda', when='+cuda')
    depends_on('cuda@9:', when='@3: +cuda')

    def cmake_args(self):

        carch = self.spec.variants['cuda_arch'].value[0]

        args = [
            '-DCMAKE_C_FLAGS=-g',
            '-DCMAKE_CXX_FLAGS=-g',
            '-DGUI=%s' % ('+gui' in self.spec),
            '-DDoublePrec_CPU=%s' % ('+double' in self.spec),
            '-DDoublePrec_GPU=%s' % ('+double-gpu' in self.spec),
        ]

        if '+cuda' in self.spec:
            # relion+cuda requires selecting cuda_arch
            if not carch:
                raise ValueError("select cuda_arch when building with +cuda")
            else:
                args += ['-DCUDA=ON', '-DCudaTexture=ON',
                         '-DCUDA_ARCH=%s' % (carch)]

        # these new values were added in relion 3
        # do not seem to cause problems with < 3
        else:
            args += ['-DMKLFFT=ON', '-DFORCE_OWN_TBB=ON', '-DALTCPU=ON']

        return args

    def patch(self):
        # Remove flags not recognized by the NVIDIA compilers
        if self.spec.satisfies('%nvhpc'):
            filter_file('-std=c99', '-c99', 'src/apps/CMakeLists.txt')
