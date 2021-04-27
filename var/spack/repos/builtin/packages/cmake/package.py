# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re


class Cmake(Package):
    """A cross-platform, open-source build system. CMake is a family of
    tools designed to build, test and package software.
    """
    homepage = 'https://www.cmake.org'
    url = 'https://github.com/Kitware/CMake/releases/download/v3.19.0/cmake-3.19.0.tar.gz'
    maintainers = ['chuckatkins']

    tags = ['build-tools']

    executables = ['^cmake$']

    version('3.20.1',   sha256='3f1808b9b00281df06c91dd7a021d7f52f724101000da7985a401678dfe035b0')
    version('3.20.0',   sha256='9c06b2ddf7c337e31d8201f6ebcd3bba86a9a033976a9aee207fe0c6971f4755')
    version('3.19.8',   sha256='09b4fa4837aae55c75fb170f6a6e2b44818deba48335d1969deddfbb34e30369')
    version('3.19.7',   sha256='58a15f0d56a0afccc3cc5371234fce73fcc6c8f9dbd775d898e510b83175588e')
    version('3.19.6',   sha256='ec87ab67c45f47c4285f204280c5cde48e1c920cfcfed1555b27fb3b1a1d20ba')
    version('3.19.5',   sha256='c432296eb5dec6d71eae15d140f6297d63df44e9ffe3e453628d1dc8fc4201ce')
    version('3.19.4',   sha256='7d0232b9f1c57e8de81f38071ef8203e6820fe7eec8ae46a1df125d88dbcc2e1')
    version('3.19.3',   sha256='3faca7c131494a1e34d66e9f8972ff5369e48d419ea8ceaa3dc15b4c11367732')
    version('3.19.2',   sha256='e3e0fd3b23b7fb13e1a856581078e0776ffa2df4e9d3164039c36d3315e0c7f0')
    version('3.19.1',   sha256='1d266ea3a76ef650cdcf16c782a317cb4a7aa461617ee941e389cb48738a3aba')
    version('3.19.0',   sha256='fdda688155aa7e72b7c63ef6f559fca4b6c07382ea6dca0beb5f45aececaf493')
    version('3.18.6',   sha256='124f571ab70332da97a173cb794dfa09a5b20ccbb80a08e56570a500f47b6600')
    version('3.18.5',   sha256='080bf24b0f73f4bf3ec368d2be1aa59369b9bb1cd693deeb6f18fe553ca74ab4')
    version('3.18.4',   sha256='597c61358e6a92ecbfad42a9b5321ddd801fc7e7eca08441307c9138382d4f77')
    version('3.18.3',   sha256='2c89f4e30af4914fd6fb5d00f863629812ada848eee4e2d29ec7e456d7fa32e5')
    version('3.18.2',   sha256='5d4e40fc775d3d828c72e5c45906b4d9b59003c9433ff1b36a1cb552bbd51d7e')
    version('3.18.1',   sha256='c0e3338bd37e67155b9d1e9526fec326b5c541f74857771b7ffed0c46ad62508')
    version('3.18.0',   sha256='83b4ffcb9482a73961521d2bafe4a16df0168f03f56e6624c419c461e5317e29')
    version('3.17.5',   sha256='8c3083d98fd93c1228d5e4e40dbff2dd88f4f7b73b9fa24a2938627b8bc28f1a')
    version('3.17.4',   sha256='86985d73d0a63ec99c236aab5287316e252164f33d7c4cb160954a980c71f36f')
    version('3.17.3',   sha256='0bd60d512275dc9f6ef2a2865426a184642ceb3761794e6b65bff233b91d8c40')
    version('3.17.1',   sha256='3aa9114485da39cbd9665a0bfe986894a282d5f0882b1dea960a739496620727')
    version('3.17.0',   sha256='b74c05b55115eacc4fa2b77a814981dbda05cdc95a53e279fe16b7b272f00847')
    version('3.16.9',   sha256='1708361827a5a0de37d55f5c9698004c035abb1de6120a376d5d59a81630191f')
    version('3.16.8',   sha256='177434021132686cb901fea7db9fa2345efe48d566b998961594d5cc346ac588')
    version('3.16.7',   sha256='5f49c95a2933b1800f14840f3a389f4cef0b19093985a35053b43f38ec21358f')
    version('3.16.6',   sha256='6f6ff1a197851b0fa8412ff5de602e6717a4eb9509b2c385b08589c4e7a16b62')
    version('3.16.5',   sha256='5f760b50b8ecc9c0c37135fae5fbf00a2fef617059aa9d61c1bb91653e5a8bfc')
    version('3.16.4',   sha256='9bcc8c114d9da603af9512083ed7d4a39911d16105466beba165ba8fe939ac2c')
    version('3.16.3',   sha256='e54f16df9b53dac30fd626415833a6e75b0e47915393843da1825b096ee60668')
    version('3.16.2',   sha256='8c09786ec60ca2be354c29829072c38113de9184f29928eb9da8446a5f2ce6a9')
    version('3.16.1',   sha256='a275b3168fa8626eca4465da7bb159ff07c8c6cb0fb7179be59e12cbdfa725fd')
    version('3.16.0',   sha256='6da56556c63cab6e9a3e1656e8763ed4a841ac9859fefb63cbe79472e67e8c5f')
    version('3.15.7',   sha256='71999d8a14c9b51708847371250a61533439a7331eb7702ac105cfb3cb1be54b')
    version('3.15.6',   sha256='3fa17992ac97d3fc856ffba5d3b10578744ea5b4736818f01e6067f0253b2db5')
    version('3.15.5',   sha256='fbdd7cef15c0ced06bb13024bfda0ecc0dedbcaaaa6b8a5d368c75255243beb4')
    version('3.15.4',   sha256='8a211589ea21374e49b25fc1fc170e2d5c7462b795f1b29c84dd0e984301ed7a')
    version('3.15.3',   sha256='13958243a01365b05652fa01b21d40fa834f70a9e30efa69c02604e64f58b8f5')
    version('3.15.2',   sha256='539088cb29a68e6d6a8fba5c00951e5e5b1a92c68fa38a83e1ed2f355933f768')
    version('3.15.1',   sha256='18dec548d8f8b04d53c60f9cedcebaa6762f8425339d1e2c889c383d3ccdd7f7')
    version('3.15.0',   sha256='0678d74a45832cacaea053d85a5685f3ed8352475e6ddf9fcb742ffca00199b5')
    version('3.14.7',   sha256='9221993e0af3e6d10124d840ff24f5b2f3b884416fca04d3312cb0388dec1385')
    version('3.14.6',   sha256='4e8ea11cabe459308671b476469eace1622e770317a15951d7b55a82ccaaccb9')
    version('3.14.5',   sha256='505ae49ebe3c63c595fa5f814975d8b72848447ee13b6613b0f8b96ebda18c06')
    version('3.14.4',   sha256='00b4dc9b0066079d10f16eed32ec592963a44e7967371d2f5077fd1670ff36d9')
    version('3.14.3',   sha256='215d0b64e81307182b29b63e562edf30b3875b834efdad09b3fcb5a7d2f4b632')
    version('3.14.2',   sha256='a3cbf562b99270c0ff192f692139e98c605f292bfdbc04d70da0309a5358e71e')
    version('3.14.1',   sha256='7321be640406338fc12590609c42b0fae7ea12980855c1be363d25dcd76bb25f')
    version('3.14.0',   sha256='aa76ba67b3c2af1946701f847073f4652af5cbd9f141f221c97af99127e75502')
    version('3.13.5',   sha256='526db6a4b47772d1943b2f86de693e712f9dacf3d7c13b19197c9bef133766a5')
    version('3.13.4',   sha256='fdd928fee35f472920071d1c7f1a6a2b72c9b25e04f7a37b409349aef3f20e9b')
    version('3.13.3',   sha256='665f905036b1f731a2a16f83fb298b1fb9d0f98c382625d023097151ad016b25')
    version('3.13.2',   sha256='c925e7d2c5ba511a69f43543ed7b4182a7d446c274c7480d0e42cd933076ae25')
    version('3.13.1',   sha256='befe1ce6d672f2881350e94d4e3cc809697dd2c09e5b708b76c1dae74e1b2210')
    version('3.13.0',   sha256='4058b2f1a53c026564e8936698d56c3b352d90df067b195cb749a97a3d273c90')
    version('3.12.4',   sha256='5255584bfd043eb717562cff8942d472f1c0e4679c4941d84baadaa9b28e3194')
    version('3.12.3',   sha256='acbf13af31a741794106b76e5d22448b004a66485fc99f6d7df4d22e99da164a')
    version('3.12.2',   sha256='0f97485799e51a7070cc11494f3e02349b0fc3a24cc12b082e737bf67a0581a4')
    version('3.12.1',   sha256='c53d5c2ce81d7a957ee83e3e635c8cda5dfe20c9d501a4828ee28e1615e57ab2')
    version('3.12.0',   sha256='d0781a90f6cdb9049d104ac16a150f9350b693498b9dea8a0331e799db6b9d69')
    version('3.11.4',   sha256='8f864e9f78917de3e1483e256270daabc4a321741592c5b36af028e72bff87f5')
    version('3.11.3',   sha256='287135b6beb7ffc1ccd02707271080bbf14c21d80c067ae2c0040e5f3508c39a')
    version('3.11.2',   sha256='5ebc22bbcf2b4c7a20c4190d42c084cf38680a85b1a7980a2f1d5b4a52bf5248')
    version('3.11.1',   sha256='57bebc6ca4d1d42c6385249d148d9216087e0fda57a47dc5c858790a70217d0c')
    version('3.11.0',   sha256='c313bee371d4d255be2b4e96fd59b11d58bc550a7c78c021444ae565709a656b')
    version('3.10.3',   sha256='0c3a1dcf0be03e40cf4f341dda79c96ffb6c35ae35f2f911845b72dab3559cf8')
    version('3.10.2',   sha256='80d0faad4ab56de07aa21a7fc692c88c4ce6156d42b0579c6962004a70a3218b')
    version('3.10.1',   sha256='7be36ee24b0f5928251b644d29f5ff268330a916944ef4a75e23ba01e7573284')
    version('3.10.0',   sha256='b3345c17609ea0f039960ef470aa099de9942135990930a57c14575aae884987')
    version('3.9.6',    sha256='7410851a783a41b521214ad987bb534a7e4a65e059651a2514e6ebfc8f46b218')
    version('3.9.4',    sha256='b5d86f12ae0072db520fdbdad67405f799eb728b610ed66043c20a92b4906ca1')
    version('3.9.2',    sha256='954a5801a456ee48e76f01107c9a4961677dd0f3e115275bbd18410dc22ba3c1')
    version('3.9.0',    sha256='167701525183dbb722b9ffe69fb525aa2b81798cf12f5ce1c020c93394dfae0f')
    version('3.8.2',    sha256='da3072794eb4c09f2d782fcee043847b99bb4cf8d4573978d9b2024214d6e92d')
    version('3.8.1',    sha256='ce5d9161396e06501b00e52933783150a87c33080d4bdcef461b5b7fd24ac228')
    version('3.8.0',    sha256='cab99162e648257343a20f61bcd0b287f5e88e36fcb2f1d77959da60b7f35969')
    version('3.7.2',    sha256='dc1246c4e6d168ea4d6e042cfba577c1acd65feea27e56f5ff37df920c30cae0')
    version('3.7.1',    sha256='449a5bce64dbd4d5b9517ebd1a1248ed197add6ad27934478976fd5f1f9330e1')
    version('3.6.1',    sha256='28ee98ec40427d41a45673847db7a905b59ce9243bb866eaf59dce0f58aaef11')
    version('3.6.0',    sha256='fd05ed40cc40ef9ef99fac7b0ece2e0b871858a82feade48546f5d2940147670')
    version('3.5.2',    sha256='92d8410d3d981bb881dfff2aed466da55a58d34c7390d50449aa59b32bb5e62a')
    version('3.5.1',    sha256='93d651a754bcf6f0124669646391dd5774c0fc4d407c384e3ae76ef9a60477e8')
    version('3.5.0',    sha256='92c83ad8a4fd6224cf6319a60b399854f55b38ebe9d297c942408b792b1a9efa')
    version('3.4.3',    sha256='b73f8c1029611df7ed81796bf5ca8ba0ef41c6761132340c73ffe42704f980fa')
    version('3.4.0',    sha256='a5b82bf6ace6c481cdb911fd5d372a302740cbefd387e05297cb37f7468d1cea')
    version('3.3.1',    sha256='cd65022c6a0707f1c7112f99e9c981677fdd5518f7ddfa0f778d4cee7113e3d6')
    version('3.1.0',    sha256='8bdc3fa3f2da81bc10c772a6b64cc9052acc2901d42e1e1b2588b40df224aad9')
    version('3.0.2',    sha256='6b4ea61eadbbd9bec0ccb383c29d1f4496eacc121ef7acf37c7a24777805693e')
    version('2.8.10.2', sha256='ce524fb39da06ee6d47534bbcec6e0b50422e18b62abc4781a4ba72ea2910eb1')

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    # Revert the change that introduced a regression when parsing mpi link
    # flags, see: https://gitlab.kitware.com/cmake/cmake/issues/19516
    patch('cmake-revert-findmpi-link-flag-list.patch', when='@3.15.0')

    # Fix linker error when using external libs on darwin.
    # See https://gitlab.kitware.com/cmake/cmake/merge_requests/2873
    patch('cmake-macos-add-coreservices.patch', when='@3.11.0:3.13.3')

    # Fix builds with XLF + Ninja generator
    # https://gitlab.kitware.com/cmake/cmake/merge_requests/4075
    patch('fix-xlf-ninja-mr-4075.patch', sha256="42d8b2163a2f37a745800ec13a96c08a3a20d5e67af51031e51f63313d0dedd1", when="@3.15.5")

    # We default ownlibs to true because it greatly speeds up the CMake
    # build, and CMake is built frequently. Also, CMake is almost always
    # a build dependency, and its libs will not interfere with others in
    # the build.
    variant('ownlibs', default=True,  description='Use CMake-provided third-party libraries')
    variant('qt',      default=False, description='Enables the build of cmake-gui')
    variant('doc',     default=False, description='Enables the generation of html and man page documentation')
    variant('openssl', default=True,  description="Enables CMake's OpenSSL features")
    variant('ncurses', default=True,  description='Enables the build of the ncurses gui')

    # Does not compile and is not covered in upstream CI (yet).
    conflicts('%gcc platform=darwin',
              msg='CMake does not compile with GCC on macOS yet, '
                  'please use %apple-clang. '
                  'See: https://gitlab.kitware.com/cmake/cmake/-/issues/21135')

    conflicts('%nvhpc')

    # Really this should conflict since it's enabling or disabling openssl for
    # CMake's internal copy of curl.  Ideally we'd want a way to have the
    # openssl variant disabled when ~ownlibs but there's not really a way to
    # tie the values of those togethor, so for now we're just going to ignore
    # the openssl variant entirely when ~ownlibs
    # conflicts('~ownlibs', when='+openssl')

    depends_on('curl',           when='~ownlibs')
    depends_on('expat',          when='~ownlibs')
    depends_on('zlib',           when='~ownlibs')
    depends_on('bzip2',          when='~ownlibs')
    depends_on('xz',             when='~ownlibs')
    depends_on('libarchive@3.1.0:', when='~ownlibs')
    depends_on('libarchive@3.3.3:',     when='@3.15.0:~ownlibs')
    depends_on('libuv@1.0.0:1.10.99',   when='@3.7.0:3.10.3~ownlibs')
    depends_on('libuv@1.10.0:1.10.99',  when='@3.11.0:3.11.99~ownlibs')
    depends_on('libuv@1.10.0:',  when='@3.12.0:~ownlibs')
    depends_on('rhash',          when='@3.8.0:~ownlibs')
    depends_on('qt',             when='+qt')
    depends_on('python@2.7.11:', when='+doc', type='build')
    depends_on('py-sphinx',      when='+doc', type='build')
    depends_on('openssl', when='+openssl')
    depends_on('openssl@:1.0.99', when='@:3.6.9+openssl')
    depends_on('ncurses',        when='+ncurses')

    # Cannot build with Intel, should be fixed in 3.6.2
    # https://gitlab.kitware.com/cmake/cmake/issues/16226
    patch('intel-c-gnu11.patch', when='@3.6.0:3.6.1')

    # Cannot build with Intel again, should be fixed in 3.17.4 and 3.18.1
    # https://gitlab.kitware.com/cmake/cmake/-/issues/21013
    patch('intel-cxx-bootstrap.patch', when='@3.17.0:3.17.3,3.18.0')

    # https://gitlab.kitware.com/cmake/cmake/issues/18232
    patch('nag-response-files.patch', when='@3.7:3.12')

    # Cray libhugetlbfs and icpc warnings failing CXX tests
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/4698
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/4681
    patch('ignore_crayxc_warnings.patch', when='@3.7:3.17.2')

    # The Fujitsu compiler requires the '--linkfortran' option
    # to combine C++ and Fortran programs.
    patch('fujitsu_add_linker_option.patch', when='%fj')

    # Remove -A from the C++ flags we use when CXX_EXTENSIONS is OFF
    # Should be fixed in 3.19.
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/5025
    patch('pgi-cxx-ansi.patch', when='@3.15:3.18.99')

    # Adds CCE v11+ fortran preprocessing definition.
    # requires Cmake 3.19+
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/5882
    patch('5882-enable-cce-fortran-preprocessing.patch',
          sha256='b48396c0e4f61756248156b6cebe9bc0d7a22228639b47b5aa77c9330588ce88',
          when='@3.19.0:3.19.99')

    conflicts('+qt', when='^qt@5.4.0')  # qt-5.4.0 has broken CMake modules

    # https://gitlab.kitware.com/cmake/cmake/issues/18166
    conflicts('%intel', when='@3.11.0:3.11.4')
    conflicts('%intel@:14', when='@3.14:',
              msg="Intel 14 has immature C++11 support")

    phases = ['bootstrap', 'build', 'install']

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'cmake.*version\s+(\S+)', output)
        return match.group(1) if match else None

    def flag_handler(self, name, flags):
        if name == 'cxxflags' and self.compiler.name == 'fj':
            cxx11plus_flags = (self.compiler.cxx11_flag,
                               self.compiler.cxx14_flag)
            cxxpre11_flags = (self.compiler.cxx98_flag)
            if any(f in flags for f in cxxpre11_flags):
                raise ValueError('cannot build cmake pre-c++11 standard')
            elif not any(f in flags for f in cxx11plus_flags):
                flags.append(self.compiler.cxx11_flag)
        return (flags, None, None)

    def bootstrap_args(self):
        spec = self.spec
        args = [
            'CFLAGS=-O3',
            'CXXFLAGS=-O3',
            '--prefix={0}'.format(self.prefix),
            '--parallel={0}'.format(make_jobs)
        ]

        if '+ownlibs' in spec:
            # Build and link to the CMake-provided third-party libraries
            args.append('--no-system-libs')
        else:
            # Build and link to the Spack-installed third-party libraries
            args.append('--system-libs')

            if spec.satisfies('@3.2:'):
                # jsoncpp requires CMake to build
                # use CMake-provided library to avoid circular dependency
                args.append('--no-system-jsoncpp')

        if '+qt' in spec:
            args.append('--qt-gui')
        else:
            args.append('--no-qt-gui')

        if '+doc' in spec:
            args.append('--sphinx-html')
            args.append('--sphinx-man')

        # Now for CMake arguments to pass after the initial bootstrap
        args.append('--')

        args.append('-DCMAKE_BUILD_TYPE={0}'.format(
            self.spec.variants['build_type'].value))

        # Install CMake correctly, even if `spack install` runs
        # inside a ctest environment
        args.append('-DCMake_TEST_INSTALL=OFF')

        # When building our own private copy of curl then we need to properly
        # enable / disable oepnssl
        if '+ownlibs' in spec:
            args.append('-DCMAKE_USE_OPENSSL=%s' % str('+openssl' in spec))

        return args

    def bootstrap(self, spec, prefix):
        bootstrap = Executable('./bootstrap')
        bootstrap(*self.bootstrap_args())

    def build(self, spec, prefix):
        make()

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def build_test(self):
        # Some tests fail, takes forever
        make('test')

    def install(self, spec, prefix):
        make('install')

        if spec.satisfies('%fj'):
            for f in find(self.prefix, 'FindMPI.cmake', recursive=True):
                filter_file('mpcc_r)', 'mpcc_r mpifcc)', f, string=True)
                filter_file('mpc++_r)', 'mpc++_r mpiFCC)', f, string=True)
                filter_file('mpifc)', 'mpifc mpifrt)', f, string=True)

    def test(self):
        """Perform smoke tests on the installed package."""
        spec_vers_str = 'version {0}'.format(self.spec.version)

        for exe in ['ccmake', 'cmake', 'cpack', 'ctest']:
            reason = 'test version of {0} is {1}'.format(exe, spec_vers_str)
            self.run_test(exe, ['--version'], [spec_vers_str],
                          installed=True, purpose=reason, skip_missing=True)
