# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sgpp(SConsPackage):
    """SGpp is a library and framework for sparse grids in different flavors.
    SGpp supports both hierarchical spatially-adaptive sparse grids and the
    dimensionally-adaptive sparse grid combination technique."""

    homepage = "https://sgpp.sparsegrids.org"
    url = "https://github.com/SGpp/SGpp/archive/v3.2.0.tar.gz"
    git = "https://github.com/SGpp/SGpp.git"

    maintainers = ['G-071', 'leiterrl', 'pfluegdk']

    # Versions with Python 3 bindings:
    version('master', branch='master')
    version('3.3.0', sha256='ca4d5b79f315b425ce69b04940c141451a76848bf1bd7b96067217304c68e2d4')
    version('3.2.0', sha256='dab83587fd447f92ed8546eacaac6b8cbe65b8db5e860218c0fa2e42f776962d')
    # Versions with Python 2 bindings:
    version('3.1.0', sha256='6b46bc5b3966e92567d6754130666bdffb7be1d1d2c1b427d7ce964b8eaab526')
    version('3.0.0', sha256='4dd9049e664abd7db78c355fea5e192167812f443115d4bf686a51bb1e9bda9c')

    # Patches with bugfixes that are necessary to build old SGpp versions
    # with spack. Patches are submitted upstream, but need to applied
    # for versions too old to include them as they will not be
    # backported for old releases:

    # Patch that ensures libraries will actually
    # be copied into prefix/lib upon installation
    # (otherwise it would be prefix/lib/sgpp)
    # Fixed in SGpp in PR https://github.com/SGpp/SGpp/pull/222
    patch('directory.patch', when='@1.0.0:3.2.0')
    # Fix faulty setup.py introduced in 3.2.0
    # Fixed in SGpp in version 3.3.0
    patch('fix-setup-py.patch', when='@3.2.0')
    # Fix compilation issue with opencl introduced in 3.2.0
    # Fixed in SGpp in PR https://github.com/SGpp/SGpp/pull/219
    patch('ocl.patch', when='@3.2.0+opencl')
    # Fixes compilation with AVX512 and datadriven
    # Fixed in SGpp in PR https://github.com/SGpp/SGpp/pull/229
    patch('avx512_datadriven_compilation.patch', when='@:3.3.0+datadriven')

    variant('python', default=True,
            description='Provide Python bindings for SGpp')
    variant('optimization', default=True,
            description='Builds the optimization module of SGpp')
    variant('pde', default=True,
            description='Builds the datadriven module of SGpp')
    variant('quadrature', default=True,
            description='Builds the datadriven module of SGpp')
    variant('datadriven', default=False,
            description='Builds the datadriven module of SGpp')
    variant('misc', default=False,
            description='Builds the misc module of SGpp')
    variant('combigrid', default=False,
            description='Builds the combigrid module of SGpp')
    variant('solver', default=True,
            description='Builds the solver module of SGpp')
    variant('opencl', default=False,
            description='Enables support for OpenCL accelerated operations')
    variant('mpi', default=False,
            description='Enables support for MPI-distributed operations')

    # Java variant deactivated due to spack issue #987
    # variant('java', default=False,
    #         description='Provide Java bindings for SGpp')
    # depends_on('swig@3:', when='+java', type=('build'))
    # extends('openjdk', when='+java')

    # Mandatory dependencies
    depends_on('scons', type=('build'))
    depends_on('scons@2.5.1', when='@1.0.0:3.1.0', type=('build'))
    depends_on('scons@3:', when='@3.2.0:', type=('build'))
    depends_on('zlib', type=('link'))
    # Python dependencies
    extends('python', when='+python')
    depends_on('py-setuptools', when='+python', type=('build'))
    # Python 3 support was added in version 3.2.0
    depends_on('python', when='+python', type=('build', 'run'))
    depends_on('python@2.7:2.8', when='@1.0.0:3.1.0+python', type=('build', 'run'))
    depends_on('python@3:', when='@3.2.0:+python', type=('build', 'run'))
    depends_on('swig@3:', when='+python', type=('build'))
    # Python libraries (version depends on whether we use Python 2 or 3)
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('py-numpy@:1.16', when='@1.0.0:3.1.0+python', type=('build', 'run'))
    depends_on('py-numpy@1.17:', when='@3.2.0:+python', type=('build', 'run'))
    depends_on('py-scipy', when='+python', type=('build', 'run'))
    depends_on('py-scipy@:1.2.3', when='@1.0.0:3.1.0+python', type=('build', 'run'))
    depends_on('py-scipy@1.3.0:', when='@3.2.0:+python', type=('build', 'run'))
    # OpenCL dependency
    depends_on('opencl@1.1:', when='+opencl', type=('build', 'run'))
    # MPI dependency
    depends_on('mpi', when='+mpi', type=('build', 'run'))
    # Testing requires boost test
    depends_on('boost+test', type=('test'))

    # Compiler with C++11 support is required
    conflicts('%gcc@:4.8.4', msg='Compiler with c++11 support is required!')
    conflicts('%apple-clang@:3.9', msg='Compiler with c++11 support is required!')
    conflicts('%clang@:3.2', msg='Compiler with c++11 support is required!')
    conflicts('%intel@:14', msg='Compiler with c++11 support is required!')
    # Solver python bindings are actually using the pde module at one point:
    conflicts('-pde', when='+python+solver')
    # some modules depend on each other (notably datadriven and misc)
    conflicts('+pde', when='-solver')
    # Datadriven module requirements
    conflicts('+datadriven', when='-solver')
    conflicts('+datadriven', when='-optimization')
    conflicts('+datadriven', when='-pde')
    # Misc module requirements
    conflicts('+misc', when='-datadriven')
    conflicts('+misc', when='-solver')
    conflicts('+misc', when='-optimization')
    conflicts('+misc', when='-pde')
    conflicts('+misc', when='@1.0.0:3.1.0',
              msg='The misc module was introduced in version 3.2.0')
    # Combigrid module requirements (for 3.2.0 or older)
    # newer combigrids have no dependencies
    conflicts('+combigrid', when='@1.0.0:3.2.0~optimization')
    conflicts('+combigrid', when='@1.0.0:3.2.0~pde')
    conflicts('+combigrid', when='@1.0.0:3.2.0~solver')
    conflicts('+combigrid', when='@1.0.0:3.2.0~quadrature')

    patch('for_aarch64.patch', when='target=aarch64:')

    def build_args(self, spec, prefix):
        # Testing parameters
        if self.run_tests:
            self.args = ['COMPILE_BOOST_TESTS=1',
                         'RUN_BOOST_TESTS=1']
            if ('+python' in spec):
                self.args.append('RUN_PYTHON_TESTS=1')
            if spec.satisfies('@1.0.0:3.2.0'):
                self.args.append('RUN_CPPLINT=1')
            else:  # argument was renamed after 3.2.0
                self.args.append('CHECK_STYLE=1')
        else:
            self.args = ['COMPILE_BOOST_TESTS=0',
                         'RUN_BOOST_TESTS=0',
                         'RUN_PYTHON_TESTS=0']
            if spec.satisfies('@1.0.0:3.2.0'):
                self.args.append('RUN_CPPLINT=0')
            else:  # argument was renamed after 3.2.0
                self.args.append('CHECK_STYLE=0')

        # Install direction
        self.args.append('PREFIX={0}'.format(prefix))

        # Generate swig bindings?
        self.args.append('SG_PYTHON={0}'.format(
            '1' if '+python' in spec else '0'))

        # Java variant deactivated due to spack issue #987
        # self.args.append('SG_JAVA={0}'.format(
        #     '1' if '+java' in spec else '0'))
        self.args.append('SG_JAVA=0')

        # Which modules to build?
        self.args.append('SG_OPTIMIZATION={0}'.format(
            '1' if '+optimization' in spec else '0'))
        self.args.append('SG_QUADRATURE={0}'.format(
            '1' if '+quadrature' in spec else '0'))
        self.args.append('SG_PDE={0}'.format(
            '1' if '+pde' in spec else '0'))
        self.args.append('SG_DATADRIVEN={0}'.format(
            '1' if '+datadriven' in spec else '0'))
        self.args.append('SG_COMBIGRID={0}'.format(
            '1' if '+combigrid' in spec else '0'))
        self.args.append('SG_SOLVER={0}'.format(
            '1' if '+solver' in spec else '0'))

        # Misc flag did not exist in older versions
        if not spec.satisfies('@1.0.0:3.2.0'):
            self.args.append('SG_MISC={0}'.format(
                '1' if '+misc' in spec else '0'))

        # SIMD scons parameter (pick according to simd spec)
        if 'avx512' in self.spec.target:
            self.args.append('ARCH=avx512')
        elif 'avx2' in self.spec.target:
            self.args.append('ARCH=avx2')
        elif 'avx' in self.spec.target:
            self.args.append('ARCH=avx')
        elif 'fma4' in self.spec.target:
            self.args.append('ARCH=fma4')
        elif 'sse42' in self.spec.target:
            self.args.append('ARCH=sse42')
        elif 'sse3' in self.spec.target:
            self.args.append('ARCH=sse3')

        # OpenCL Flags
        self.args.append('USE_OCL={0}'.format(
            '1' if '+opencl' in spec else '0'))

        # Get the mpicxx compiler from the Spack spec
        # (makes certain we use the one from spack):
        if ('+mpi' in spec):
            self.args.append('CXX={0}'.format(
                self.spec['mpi'].mpicxx))
        else:
            self.args.append('CXX={0}'.format(self.compiler.cxx))

        return self.args

    def install_args(self, spec, prefix):
        # Everything is already built, time to install our python bindings:
        if '+python' in spec:
            setup_py('install', '--prefix={0}'.format(prefix))
        return self.args
