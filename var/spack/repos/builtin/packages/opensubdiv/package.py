# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Opensubdiv(CMakePackage, CudaPackage):
    """OpenSubdiv is a set of open source libraries that
    implement high performance subdivision surface (subdiv)
    evaluation on massively parallel CPU and GPU architectures.
    This code path is optimized for drawing deforming surfaces
    with static topology at interactive framerates."""

    homepage = "http://graphics.pixar.com/opensubdiv/docs/intro.html"
    url      = "https://github.com/PixarAnimationStudios/OpenSubdiv/archive/v3_4_0.tar.gz"
    git      = "https://github.com/PixarAnimationStudios/OpenSubdiv"

    version('develop', branch='dev')
    version('3_4_0',     sha256='d932b292f83371c7518960b2135c7a5b931efb43cdd8720e0b27268a698973e4')

    variant('tbb', default=False, description='Builds with Intel TBB support')
    variant('openmp', default=False, description='Builds with OpenMP support')
    variant('doc', default=False, description='Builds documentation. Requires Python 2')

    depends_on('cmake@2.8.6:', type='build')
    depends_on('graphviz', type='build', when='+doc')
    depends_on('doxygen', type='build', when='+doc')
    depends_on('py-docutils', type='build', when='+doc')
    depends_on('python@2.6:2.999', type='build', when='+doc')
    depends_on('gl')
    depends_on('glew@1.9.0:')
    depends_on('glfw@3.0.0:')
    depends_on('intel-tbb@4.0:', when='+tbb')
    depends_on('libxrandr')
    depends_on('libxcursor')
    depends_on('libxinerama')
    depends_on('llvm-openmp', when='+openmp')

    def cmake_args(self):
        spec = self.spec
        args = []

        args.append('-DNO_EXAMPLES=1')    # disable examples build
        args.append('-DNO_TUTORIALS=1')   # disable tutorials build
        args.append('-DNO_REGRESSION=1')  # disable regression tests build
        args.append('-DNO_PTEX=1')        # disable PTex support
        args.append('-DNO_OPENCL=1')      # disable OpenCL
        args.append('-DNO_CLEW=1')        # disable CLEW wrapper library
        args.append('-DNO_METAL=1')       # disable Metal

        args.append('-DNO_OPENGL=0')      # OpenGL always on
        args.append('-DGLEW_LOCATION={0}'.format(spec['glew'].prefix))

        if '+cuda' in spec:
            args.append('-DNO_CUDA=0')

            cuda_arch = [x for x in spec.variants['cuda_arch'].value if x]
            if cuda_arch:
                args.append('-DOSD_CUDA_NVCC_FLAGS={0}'.format(
                    ' '.join(self.cuda_flags(cuda_arch))))
            else:
                args.append('-DOSD_CUDA_NVCC_FLAGS=')

        else:
            args.append('-DNO_CUDA=1')

        if '+tbb' in spec:
            args.append('-DNO_TBB=0')
        else:
            args.append('-DNO_TBB=1')

        if '+doc' in spec:
            args.append('-DNO_DOC=0')
        else:
            args.append('-DNO_DOC=1')

        if '+openmp' in spec:
            args.append('-DNO_OMP=0')
        else:
            args.append('-DNO_OMP=1')

        return args
