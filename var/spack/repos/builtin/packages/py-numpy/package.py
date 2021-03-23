# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import platform
import subprocess


class PyNumpy(PythonPackage):
    """NumPy is the fundamental package for scientific computing with Python.
    It contains among other things: a powerful N-dimensional array object,
    sophisticated (broadcasting) functions, tools for integrating C/C++ and
    Fortran code, and useful linear algebra, Fourier transform, and random
    number capabilities"""

    homepage = "https://numpy.org/"
    pypi = "numpy/numpy-1.19.4.zip"
    git      = "https://github.com/numpy/numpy.git"

    maintainers = ['adamjstewart']

    version('master', branch='master')
    version('1.20.1', sha256='3bc63486a870294683980d76ec1e3efc786295ae00128f9ea38e2c6e74d5a60a')
    version('1.20.0', sha256='3d8233c03f116d068d5365fed4477f2947c7229582dad81e5953088989294cec')
    version('1.19.5', sha256='a76f502430dd98d7546e1ea2250a7360c065a5fdea52b2dffe8ae7180909b6f4')
    version('1.19.4', sha256='141ec3a3300ab89c7f2b0775289954d193cc8edb621ea05f99db9cb181530512')
    version('1.19.3', sha256='35bf5316af8dc7c7db1ad45bec603e5fb28671beb98ebd1d65e8059efcfd3b72')
    version('1.19.2', sha256='0d310730e1e793527065ad7dde736197b705d0e4c9999775f212b03c44a8484c')
    version('1.19.1', sha256='b8456987b637232602ceb4d663cb34106f7eb780e247d51a260b84760fd8f491')
    version('1.19.0', sha256='76766cc80d6128750075378d3bb7812cf146415bd29b588616f72c943c00d598')
    version('1.18.5', sha256='34e96e9dae65c4839bd80012023aadd6ee2ccb73ce7fdf3074c62f301e63120b')
    version('1.18.4', sha256='bbcc85aaf4cd84ba057decaead058f43191cc0e30d6bc5d44fe336dc3d3f4509')
    version('1.18.3', sha256='e46e2384209c91996d5ec16744234d1c906ab79a701ce1a26155c9ec890b8dc8')
    version('1.18.2', sha256='e7894793e6e8540dbeac77c87b489e331947813511108ae097f1715c018b8f3d')
    version('1.18.1', sha256='b6ff59cee96b454516e47e7721098e6ceebef435e3e21ac2d6c3b8b02628eb77')
    version('1.18.0', sha256='a9d72d9abaf65628f0f31bbb573b7d9304e43b1e6bbae43149c17737a42764c4')
    version('1.17.5', sha256='16507ba6617f62ae3c6ab1725ae6f550331025d4d9a369b83f6d5a470446c342')
    version('1.17.4', sha256='f58913e9227400f1395c7b800503ebfdb0772f1c33ff8cb4d6451c06cabdf316')
    version('1.17.3', sha256='a0678793096205a4d784bd99f32803ba8100f639cf3b932dc63b21621390ea7e')
    version('1.17.2', sha256='73615d3edc84dd7c4aeb212fa3748fb83217e00d201875a47327f55363cef2df')
    version('1.17.1', sha256='f11331530f0eff69a758d62c2461cd98cdc2eae0147279d8fc86e0464eb7e8ca')
    version('1.17.0', sha256='951fefe2fb73f84c620bec4e001e80a80ddaa1b84dce244ded7f1e0cbe0ed34a')
    version('1.16.6', sha256='e5cf3fdf13401885e8eea8170624ec96225e2174eb0c611c6f26dd33b489e3ff')
    version('1.16.5', sha256='8bb452d94e964b312205b0de1238dd7209da452343653ab214b5d681780e7a0c')
    version('1.16.4', sha256='7242be12a58fec245ee9734e625964b97cf7e3f2f7d016603f9e56660ce479c7')
    version('1.16.3', sha256='78a6f89da87eeb48014ec652a65c4ffde370c036d780a995edaeb121d3625621')
    version('1.16.2', sha256='6c692e3879dde0b67a9dc78f9bfb6f61c666b4562fd8619632d7043fb5b691b0')
    version('1.16.1', sha256='31d3fe5b673e99d33d70cfee2ea8fe8dccd60f265c3ed990873a88647e3dd288')
    version('1.16.0', sha256='cb189bd98b2e7ac02df389b6212846ab20661f4bafe16b5a70a6f1728c1cc7cb')
    version('1.15.4', sha256='3d734559db35aa3697dadcea492a423118c5c55d176da2f3be9c98d4803fc2a7')
    version('1.15.3', sha256='1c0c80e74759fa4942298044274f2c11b08c86230b25b8b819e55e644f5ff2b6')
    version('1.15.2', sha256='27a0d018f608a3fe34ac5e2b876f4c23c47e38295c47dd0775cc294cd2614bc1')
    version('1.15.2', sha256='27a0d018f608a3fe34ac5e2b876f4c23c47e38295c47dd0775cc294cd2614bc1')
    version('1.15.1', sha256='7b9e37f194f8bcdca8e9e6af92e2cbad79e360542effc2dd6b98d63955d8d8a3')
    version('1.15.0', sha256='f28e73cf18d37a413f7d5de35d024e6b98f14566a10d82100f9dc491a7d449f9')
    version('1.14.6', sha256='1250edf6f6c43e1d7823f0967416bc18258bb271dc536298eb0ea00a9e45b80a')
    version('1.14.5', sha256='a4a433b3a264dbc9aa9c7c241e87c0358a503ea6394f8737df1683c7c9a102ac')
    version('1.14.4', sha256='2185a0f31ecaa0792264fa968c8e0ba6d96acf144b26e2e1d1cd5b77fc11a691')
    version('1.14.3', sha256='9016692c7d390f9d378fc88b7a799dc9caa7eb938163dda5276d3f3d6f75debf')
    version('1.14.2', sha256='facc6f925c3099ac01a1f03758100772560a0b020fb9d70f210404be08006bcb')
    version('1.14.1', sha256='fa0944650d5d3fb95869eaacd8eedbd2d83610c85e271bd9d3495ffa9bc4dc9c')
    version('1.14.0', sha256='3de643935b212307b420248018323a44ec51987a336d1d747c1322afc3c099fb')
    version('1.13.3', sha256='36ee86d5adbabc4fa2643a073f93d5504bdfed37a149a3a49f4dde259f35a750')
    version('1.13.1', sha256='c9b0283776085cb2804efff73e9955ca279ba4edafd58d3ead70b61d209c4fbb')
    version('1.13.0', sha256='dcff367b725586830ff0e20b805c7654c876c2d4585c0834a6049502b9d6cf7e')
    version('1.12.1', sha256='a65266a4ad6ec8936a1bc85ce51f8600634a31a258b722c9274a80ff189d9542')
    version('1.12.0', sha256='ff320ecfe41c6581c8981dce892fe6d7e69806459a899e294e4bf8229737b154')
    version('1.11.3', sha256='2e0fc5248246a64628656fe14fcab0a959741a2820e003bd15538226501b82f7')
    version('1.11.2', sha256='c1ed4d1d2a795409c7df1eb4bfee65c0e3326cfc7c57875fa39e5c7414116d9a')
    version('1.11.1', sha256='4e9c289b9d764d10353a224a5286dda3e0425b13b112719bdc3e9864ae648d79')
    version('1.11.0', sha256='9109f260850627e4b83a3c4bcef4f2f99357eb4a5eaae75dec51c32f3c197aa3')
    version('1.10.4', sha256='8ce443dc79656a9fc97a7837f1444d324aef2c9b53f31f83441f57ad1f1f3659')
    version('1.9.3',  sha256='baa074bb1c7f9c822122fb81459b7caa5fc49267ca94cca69465c8dcfd63ac79')
    version('1.9.2',  sha256='e37805754f4ebb575c434d134f6bebb8b857d9843c393f6943c7be71ef57311c')
    version('1.9.1',  sha256='2a545c0d096d86035b12160fcba5e4c0a08dcabbf902b4f867eb64deb31a2b7a')

    variant('blas',   default=True, description='Build with BLAS support')
    variant('lapack', default=True, description='Build with LAPACK support')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'link', 'run'))
    depends_on('python@2.7:2.8,3.5:', type=('build', 'link', 'run'), when='@1.16:')
    depends_on('python@3.5:', type=('build', 'link', 'run'), when='@1.17:')
    depends_on('python@3.6:', type=('build', 'link', 'run'), when='@1.19:')
    depends_on('python@3.7:', type=('build', 'link', 'run'), when='@1.20:')
    depends_on('py-setuptools', type=('build', 'run'))
    # Check pyproject.toml for updates to the required cython version
    depends_on('py-cython@0.29.13:', when='@1.18.0:', type='build')
    depends_on('py-cython@0.29.14:', when='@1.18.1:', type='build')
    depends_on('py-cython@0.29.21:', when='@1.19.1:', type='build')
    depends_on('blas',   when='+blas')
    depends_on('lapack', when='+lapack')

    depends_on('py-nose@1.0.0:', when='@:1.14', type='test')
    depends_on('py-pytest', when='@1.15:', type='test')
    depends_on('py-hypothesis', when='@1.19:', type='test')

    # Allows you to specify order of BLAS/LAPACK preference
    # https://github.com/numpy/numpy/pull/13132
    patch('blas-lapack-order.patch', when='@1.15:1.16')

    # Add Fujitsu Fortran compiler
    patch('add_fj_compiler.patch', when='@1.19.3:1.19.5%fj')
    patch('add_fj_compiler2.patch', when='@1.19.0:1.19.2%fj')
    patch('add_fj_compiler3.patch', when='@1.14.0:1.18.5%fj')
    patch('add_fj_compiler4.patch', when='@:1.13.3%fj')

    patch('check_executables.patch', when='@1.20.0:')
    patch('check_executables2.patch', when='@1.19.0:1.19.5')
    patch('check_executables3.patch', when='@1.16.0:1.18.5')
    patch('check_executables4.patch', when='@1.14.0:1.15.4')
    patch('check_executables5.patch', when='@:1.13.3')

    # GCC 4.8 is the minimum version that works
    conflicts('%gcc@:4.7', msg='GCC 4.8+ required')

    # NVHPC support added in https://github.com/numpy/numpy/pull/17344
    conflicts('%nvhpc', when='@:1.19.999')

    def flag_handler(self, name, flags):
        # -std=c99 at least required, old versions of GCC default to -std=c90
        if self.spec.satisfies('%gcc@:5.1') and name == 'cflags':
            flags.append(self.compiler.c99_flag)
        # Check gcc version in use by intel compiler
        # This will essentially check the system gcc compiler unless a gcc
        # module is already loaded.
        if self.spec.satisfies('%intel') and name == 'cflags':
            p1 = subprocess.Popen(
                [self.compiler.cc, '-v'],
                stderr=subprocess.PIPE
            )
            p2 = subprocess.Popen(
                ['grep', 'compatibility'],
                stdin=p1.stderr,
                stdout=subprocess.PIPE
            )
            p1.stderr.close()
            out, err = p2.communicate()
            gcc_version = Version(out.split()[5].decode('utf-8'))
            if gcc_version < Version('4.8'):
                raise InstallError('The GCC version that the Intel compiler '
                                   'uses must be >= 4.8. The GCC in use is '
                                   '{0}'.format(gcc_version))
            if gcc_version <= Version('5.1'):
                flags.append(self.compiler.c99_flag)
        return (flags, None, None)

    @run_before('build')
    def set_blas_lapack(self):
        # https://numpy.org/devdocs/user/building.html
        # https://github.com/numpy/numpy/blob/master/site.cfg.example

        # Skip if no BLAS/LAPACK requested
        spec = self.spec
        if '+blas' not in spec and '+lapack' not in spec:
            return

        def write_library_dirs(f, dirs):
            f.write('library_dirs = {0}\n'.format(dirs))
            if not ((platform.system() == 'Darwin') and
                    (Version(platform.mac_ver()[0]).up_to(2) == Version(
                        '10.12'))):
                f.write('rpath = {0}\n'.format(dirs))

        blas_libs = LibraryList([])
        blas_headers = HeaderList([])
        if '+blas' in spec:
            blas_libs = spec['blas'].libs
            blas_headers = spec['blas'].headers

        lapack_libs = LibraryList([])
        lapack_headers = HeaderList([])
        if '+lapack' in spec:
            lapack_libs = spec['lapack'].libs
            lapack_headers = spec['lapack'].headers

        lapackblas_libs = lapack_libs + blas_libs
        lapackblas_headers = lapack_headers + blas_headers

        blas_lib_names   = ','.join(blas_libs.names)
        blas_lib_dirs    = ':'.join(blas_libs.directories)
        blas_header_dirs = ':'.join(blas_headers.directories)

        lapack_lib_names   = ','.join(lapack_libs.names)
        lapack_lib_dirs    = ':'.join(lapack_libs.directories)
        lapack_header_dirs = ':'.join(lapack_headers.directories)

        lapackblas_lib_names   = ','.join(lapackblas_libs.names)
        lapackblas_lib_dirs    = ':'.join(lapackblas_libs.directories)
        lapackblas_header_dirs = ':'.join(lapackblas_headers.directories)

        # Tell numpy where to find BLAS/LAPACK libraries
        with open('site.cfg', 'w') as f:
            if '^intel-mkl' in spec or '^intel-parallel-studio+mkl' in spec:
                f.write('[mkl]\n')
                # FIXME: as of @1.11.2, numpy does not work with separately
                # specified threading and interface layers. A workaround is a
                # terribly bad idea to use mkl_rt. In this case Spack will no
                # longer be able to guarantee that one and the same variant of
                # Blas/Lapack (32/64bit, threaded/serial) is used within the
                # DAG. This may lead to a lot of hard-to-debug segmentation
                # faults on user's side. Users may also break working
                # installation by (unconsciously) setting environment variable
                # to switch between different interface and threading layers
                # dynamically. From this perspective it is no different from
                # throwing away RPATH's and using LD_LIBRARY_PATH throughout
                # Spack.
                f.write('libraries = {0}\n'.format('mkl_rt'))
                write_library_dirs(f, lapackblas_lib_dirs)
                f.write('include_dirs = {0}\n'.format(lapackblas_header_dirs))

            if '^blis' in spec:
                f.write('[blis]\n')
                f.write('libraries = {0}\n'.format(blas_lib_names))
                write_library_dirs(f, blas_lib_dirs)
                f.write('include_dirs = {0}\n'.format(blas_header_dirs))

            if '^openblas' in spec:
                f.write('[openblas]\n')
                f.write('libraries = {0}\n'.format(lapackblas_lib_names))
                write_library_dirs(f, lapackblas_lib_dirs)
                f.write('include_dirs = {0}\n'.format(lapackblas_header_dirs))

            if '^libflame' in spec:
                f.write('[flame]\n')
                f.write('libraries = {0}\n'.format(lapack_lib_names))
                write_library_dirs(f, lapack_lib_dirs)
                f.write('include_dirs = {0}\n'.format(lapack_header_dirs))

            if '^atlas' in spec:
                f.write('[atlas]\n')
                f.write('libraries = {0}\n'.format(lapackblas_lib_names))
                write_library_dirs(f, lapackblas_lib_dirs)
                f.write('include_dirs = {0}\n'.format(lapackblas_header_dirs))

            if '^veclibfort' in spec:
                f.write('[accelerate]\n')
                f.write('libraries = {0}\n'.format(lapackblas_lib_names))
                write_library_dirs(f, lapackblas_lib_dirs)

            if '^netlib-lapack' in spec:
                # netlib requires blas and lapack listed
                # separately so that scipy can find them
                if spec.satisfies('+blas'):
                    f.write('[blas]\n')
                    f.write('libraries = {0}\n'.format(blas_lib_names))
                    write_library_dirs(f, blas_lib_dirs)
                    f.write('include_dirs = {0}\n'.format(blas_header_dirs))
                if spec.satisfies('+lapack'):
                    f.write('[lapack]\n')
                    f.write('libraries = {0}\n'.format(lapack_lib_names))
                    write_library_dirs(f, lapack_lib_dirs)
                    f.write('include_dirs = {0}\n'.format(lapack_header_dirs))

    def setup_build_environment(self, env):
        # Tell numpy which BLAS/LAPACK libraries we want to use.
        # https://github.com/numpy/numpy/pull/13132
        # https://numpy.org/devdocs/user/building.html#accelerated-blas-lapack-libraries
        spec = self.spec

        # https://numpy.org/devdocs/user/building.html#blas
        if 'blas' not in spec:
            blas = ''
        elif spec['blas'].name == 'intel-mkl' or \
                spec['blas'].name == 'intel-parallel-studio':
            blas = 'mkl'
        elif spec['blas'].name == 'blis':
            blas = 'blis'
        elif spec['blas'].name == 'openblas':
            blas = 'openblas'
        elif spec['blas'].name == 'atlas':
            blas = 'atlas'
        elif spec['blas'].name == 'veclibfort':
            blas = 'accelerate'
        else:
            blas = 'blas'

        env.set('NPY_BLAS_ORDER', blas)

        # https://numpy.org/devdocs/user/building.html#lapack
        if 'lapack' not in spec:
            lapack = ''
        elif spec['lapack'].name == 'intel-mkl' or \
                spec['lapack'].name == 'intel-parallel-studio':
            lapack = 'mkl'
        elif spec['lapack'].name == 'openblas':
            lapack = 'openblas'
        elif spec['lapack'].name == 'libflame':
            lapack = 'flame'
        elif spec['lapack'].name == 'atlas':
            lapack = 'atlas'
        elif spec['lapack'].name == 'veclibfort':
            lapack = 'accelerate'
        else:
            lapack = 'lapack'

        env.set('NPY_LAPACK_ORDER', lapack)

    def build_args(self, spec, prefix):
        args = []

        # From NumPy 1.10.0 on it's possible to do a parallel build.
        # https://numpy.org/devdocs/user/building.html#parallel-builds
        if self.version >= Version('1.10.0'):
            # But Parallel build in Python 3.5+ is broken.  See:
            # https://github.com/spack/spack/issues/7927
            # https://github.com/scipy/scipy/issues/7112
            if spec['python'].version < Version('3.5'):
                args = ['-j', str(make_jobs)]

        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir('spack-test', create=True):
            python('-c', 'import numpy; numpy.test("full", verbose=2)')
