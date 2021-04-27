# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Draco(CMakePackage):
    """Draco is an object-oriented component library geared towards numerically
    intensive, radiation (particle) transport applications built for parallel
    computing hardware. It consists of semi-independent packages and a robust
    build system. """

    homepage = "https://github.com/lanl/draco"
    url = "https://github.com/lanl/Draco/archive/draco-7_1_0.zip"
    git = "https://github.com/lanl/Draco.git"
    maintainers = ['KineticTheory']

    version('develop', branch='develop')
    version('7.10.0',  sha256='3530263a23a648fc7ae65748568f0a725a8b2c9bac9a41cc3cb1250c4af579de')
    version('7.9.1',  sha256='c8fd029d5b74afc68670f7d449d60c24f2d284c9d6a944a2d3dce6efeb6ad097')
    version('7.9.0',  sha256='17b54301897da0d4f9b91fef15cc2ec5e6c65a8e8c1c09e6e7b516c0fb82b50f')
    version('7.8.0',  sha256='f6de794457441f69025619be58810bca432f3e0dd773ea9b9a7977b1dc09530d')
    version('7.7.0',  sha256='eb7fffbcba48e16524f619d261192ead129f968c59f3581f3217b89590812ddf')
    version('7.6.0',  sha256='c2c6b329620d7bcb0f2fc14371f105dfb80a84e7c5adbb34620777034b15c7c9')
    version('7.5.0',  sha256='0bb12b5f5ff60ba3087310c07da42e8d4f481ec4259daaa24ec240815a2e9dec')
    version('7.4.0',  sha256='61da2c3feace0e92c5410c9e9e613708fdf8954b1367cdc62c415329b0ddab6e')
    version('7.3.0',  sha256='dc47ef6c1e04769ea177a10fc6ddf506f3e1e8d36eb5d49f4bc38cc509e24f10')
    version('7.2.0',  sha256='ac4eac03703d4b7344fa2390a54140533c5e1f6ea0d59ef1f1d525c434ebe639')
    version('7.1.0',  sha256='eca6bb86eb930837fb5e09b76c85c200b2c1522267cc66f81f2ec11a8262b5c9')
    version('6.25.0', sha256='e27eba44f397e7d111ff9a45b518b186940f75facfc6f318d76bd0e72f987440')
    version('6.23.0', sha256='edf20308746c06647087cb4e6ae7656fd057a89091a22bcba8f17a52e28b7849')
    version('6.22.0', sha256='4d1ed54944450c4ec7d00d7ba371469506c6985922f48f780bae2580c9335b86')
    version('6.21.0', sha256='f1ac88041606cdb1dfddd3bc74db0f1e15d8fc9d0a1eed939c8aa0fa63a85b55')
    version('6.20.1', sha256='b1c51000c9557e0818014713fce70d681869c50ed9c4548dcfb2e9219c354ebe')
    version('6.20.0', sha256='a6e3142c1c90b09c4ff8057bfee974369b815122b01d1f7b57888dcb9b1128f6')

    variant('build_type', default='Release', description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))
    variant('caliper',  default=False, description='Enable caliper timers support')
    variant('cuda',     default=False, description='Enable Cuda/GPU support')
    variant('eospac',   default=True,  description='Enable EOSPAC support')
    variant('lapack',   default=True,  description='Enable LAPACK wrapper')
    variant('libquo',   default=True,  description='Enable Quo wrapper')
    variant('parmetis', default=True,  description='Enable Parmetis support')
    variant('pythontools', default=False,  description='Enable support for extra python tools')
    variant('qt',       default=False, description='Enable Qt support')
    variant('superlu_dist', default=True, description='Enable SuperLU-DIST support')

    depends_on('cmake@3.9:',  when='@:6.99',        type='build')
    depends_on('cmake@3.11:', when='@7.0.0:7.1.99', type='build')
    depends_on('cmake@3.14:', when='@7.2.0:7.6.99', type='build')
    depends_on('cmake@3.17:', when='@7.7:',         type='build')
    depends_on('cmake@3.18:', when='@7.9:',         type='build')
    depends_on('gsl')
    depends_on('mpi@3:',         type=('build', 'link', 'run'))
    depends_on('numdiff',        type='build')
    depends_on('random123@1.09', type='build')
    depends_on('python@2.7:', when='@7.7.0:',       type=('build', 'run'))
    depends_on('python@3.5:', when='@:7.6.99',      type=('build', 'run', 'test'))

    # Optional dependencies
    depends_on('caliper',     when='+caliper')
    depends_on('cuda@11.0:',  when='+cuda')
    depends_on('eospac@6.3:', when='+eospac')
    depends_on('lapack',      when='+lapack')
    depends_on('libquo@1.3.1:', when='@7.4.0:+libquo')
    depends_on('metis',       when='+parmetis')
    depends_on('parmetis',    when='+parmetis')
    depends_on('qt',          when='+qt',
               type=('build', 'link', 'run'))
    depends_on('superlu-dist@:5.99', when='@:7.6.99+superlu_dist')
    depends_on('py-matplotlib', when='+pythontools', type=('run'))

    conflicts('+cuda', when='@:7.6.99')
    conflicts('+caliper', when='@:7.7.99')

    # Fix python discovery.
    patch('d710.patch', when='@7.1.0^python@3:')
    patch('d710-python2.patch', when='@7.1.0^python@2.7:2.99')
    patch('d730.patch', when='@7.3.0:7.3.99')
    patch('d740.patch', when='@7.4.0:7.4.99')
    patch('d760-cray.patch', when='@7.6.0')
    patch('d770-nocuda.patch', when='@7.7.0')

    def url_for_version(self, version):
        url = "https://github.com/lanl/Draco/archive/draco-{0}.zip"
        return url.format(version.underscored)

    def cmake_args(self):
        options = []
        options.extend([
            '-Wno-dev',
            '-DBUILD_TESTING={0}'.format('ON' if self.run_tests else 'OFF'),
            '-DUSE_CUDA={0}'.format('ON' if '+cuda' in self.spec else 'OFF'),
            '-DUSE_QT={0}'.format('ON' if '+qt' in self.spec else 'OFF')
        ])
        return options

    def check(self):
        """Run ctest after building project."""
        with working_dir(self.build_directory):
            ctest('--output-on-failure')
