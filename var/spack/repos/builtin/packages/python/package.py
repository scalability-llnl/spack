# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import ast
import os
import platform
import re
import sys

import llnl.util.tty as tty
from llnl.util.lang import match_predicate
from llnl.util.filesystem import (force_remove, get_filetype,
                                  path_contains_subdirectory)

import spack.store
import spack.util.spack_json as sjson
from spack.util.environment import is_system_path
from spack.util.prefix import Prefix
from spack.util.provides import setup_libtirpc_build_environment
from spack import *


class Python(AutotoolsPackage):
    """The Python programming language."""

    homepage = "https://www.python.org/"
    url      = "https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz"
    list_url = "https://www.python.org/ftp/python/"
    list_depth = 1

    maintainers = ['adamjstewart']

    version('3.9.0',  sha256='df796b2dc8ef085edae2597a41c1c0a63625ebd92487adaef2fed22b567873e8')
    version('3.8.6',  sha256='313562ee9986dc369cd678011bdfd9800ef62fbf7b1496228a18f86b36428c21', preferred=True)
    version('3.8.5',  sha256='015115023c382eb6ab83d512762fe3c5502fa0c6c52ffebc4831c4e1a06ffc49')
    version('3.8.4',  sha256='32c4d9817ef11793da4d0d95b3191c4db81d2e45544614e8449255ca9ae3cc18')
    version('3.8.3',  sha256='6af6d4d2e010f9655518d0fc6738c7ff7069f10a4d2fbd55509e467f092a8b90')
    version('3.8.2',  sha256='e634a7a74776c2b89516b2e013dda1728c89c8149b9863b8cea21946daf9d561')
    version('3.8.1',  sha256='c7cfa39a43b994621b245e029769e9126caa2a93571cee2e743b213cceac35fb')
    version('3.8.0',  sha256='f1069ad3cae8e7ec467aa98a6565a62a48ef196cb8f1455a245a08db5e1792df')
    version('3.7.9',  sha256='39b018bc7d8a165e59aa827d9ae45c45901739b0bbb13721e4f973f3521c166a')
    version('3.7.8',  sha256='0e25835614dc221e3ecea5831b38fa90788b5389b99b675a751414c858789ab0')
    version('3.7.7',  sha256='8c8be91cd2648a1a0c251f04ea0bb4c2a5570feb9c45eaaa2241c785585b475a')
    version('3.7.6',  sha256='aeee681c235ad336af116f08ab6563361a0c81c537072c1b309d6e4050aa2114')
    version('3.7.5',  sha256='8ecc681ea0600bbfb366f2b173f727b205bb825d93d2f0b286bc4e58d37693da')
    version('3.7.4',  sha256='d63e63e14e6d29e17490abbe6f7d17afb3db182dbd801229f14e55f4157c4ba3')
    version('3.7.3',  sha256='d62e3015f2f89c970ac52343976b406694931742fbde2fed8d1ce8ebb4e1f8ff')
    version('3.7.2',  sha256='f09d83c773b9cc72421abba2c317e4e6e05d919f9bcf34468e192b6a6c8e328d')
    version('3.7.1',  sha256='36c1b81ac29d0f8341f727ef40864d99d8206897be96be73dc34d4739c9c9f06')
    version('3.7.0',  sha256='85bb9feb6863e04fb1700b018d9d42d1caac178559ffa453d7e6a436e259fd0d')
    version('3.6.12', sha256='12dddbe52385a0f702fb8071e12dcc6b3cb2dde07cd8db3ed60e90d90ab78693')
    version('3.6.11', sha256='96621902f89746fffc22f39749c07da7c2917b232e72352e6837d41850f7b90c')
    version('3.6.10', sha256='7034dd7cba98d4f94c74f9edd7345bac71c8814c41672c64d9044fa2f96f334d')
    version('3.6.9',  sha256='47fc92a1dcb946b9ed0abc311d3767b7215c54e655b17fd1d3f9b538195525aa')
    version('3.6.8',  sha256='7f5b1f08b3b0a595387ef6c64c85b1b13b38abef0dd871835ee923262e4f32f0')
    version('3.6.7',  sha256='b7c36f7ed8f7143b2c46153b7332db2227669f583ea0cce753facf549d1a4239')
    version('3.6.6',  sha256='7d56dadf6c7d92a238702389e80cfe66fbfae73e584189ed6f89c75bbf3eda58')
    version('3.6.5',  sha256='53a3e17d77cd15c5230192b6a8c1e031c07cd9f34a2f089a731c6f6bd343d5c6')
    version('3.6.4',  sha256='7dc453e1a93c083388eb1a23a256862407f8234a96dc4fae0fc7682020227486')
    version('3.6.3',  sha256='ab6193af1921b30f587b302fe385268510e80187ca83ca82d2bfe7ab544c6f91')
    version('3.6.2',  sha256='7919489310a5f17f7acbab64d731e46dca0702874840dadce8bd4b2b3b8e7a82')
    version('3.6.1',  sha256='aa50b0143df7c89ce91be020fe41382613a817354b33acdc6641b44f8ced3828')
    version('3.6.0',  sha256='aa472515800d25a3739833f76ca3735d9f4b2fe77c3cb21f69275e0cce30cb2b')
    version('3.5.10', sha256='3496a0daf51913718a6f10e3eda51fa43634cb6151cb096f312d48bdbeff7d3a')
    version('3.5.9',  sha256='67a1d4fc6e4540d6a092cadc488e533afa961b3c9becc74dc3d6b55cb56e0cc1')
    version('3.5.8',  sha256='18c88dfd260147bc7247e6356010e5d4916dfbfc480f6434917f88e61228177a')
    version('3.5.7',  sha256='542d94920a2a06a471a73b51614805ad65366af98145b0369bc374cf248b521b')
    version('3.5.6',  sha256='30d2ff093988e74283e1abfee823292c6b59590796b9827e95ba4940b27d26f8')
    version('3.5.5',  sha256='2f988db33913dcef17552fd1447b41afb89dbc26e3cdfc068ea6c62013a3a2a5')
    version('3.5.4',  sha256='6ed87a8b6c758cc3299a8b433e8a9a9122054ad5bc8aad43299cff3a53d8ca44')
    version('3.5.3',  sha256='d8890b84d773cd7059e597dbefa510340de8336ec9b9e9032bf030f19291565a')
    version('3.5.2',  sha256='1524b840e42cf3b909e8f8df67c1724012c7dc7f9d076d4feef2d3eff031e8a0')
    version('3.5.1',  sha256='687e067d9f391da645423c7eda8205bae9d35edc0c76ef5218dcbe4cc770d0d7')
    version('3.5.0',  sha256='584e3d5a02692ca52fce505e68ecd77248a6f2c99adf9db144a39087336b0fe0')
    version('3.4.10', sha256='217757699249ab432571b381386d441e12b433100ab5f908051fcb7cced2539d')
    version('3.4.3',  sha256='8b743f56e9e50bf0923b9e9c45dd927c071d7aa56cd46569d8818add8cf01147')
    version('3.3.6',  sha256='0a58ad1f1def4ecc90b18b0c410a3a0e1a48cf7692c75d1f83d0af080e5d2034')
    version('3.2.6',  sha256='fc1e41296e29d476f696303acae293ae7a2310f0f9d0d637905e722a3f16163e')
    version('3.1.5',  sha256='d12dae6d06f52ef6bf1271db4d5b4d14b5dd39813e324314e72b648ef1bc0103')
    version('2.7.18', sha256='da3080e3b488f648a3d7a4560ddee895284c3380b11d6de75edb986526b9a814')
    version('2.7.17', sha256='f22059d09cdf9625e0a7284d24a13062044f5bf59d93a7f3382190dfa94cecde')
    version('2.7.16', sha256='01da813a3600876f03f46db11cc5c408175e99f03af2ba942ef324389a83bad5')
    version('2.7.15', sha256='18617d1f15a380a919d517630a9cd85ce17ea602f9bbdc58ddc672df4b0239db')
    version('2.7.14', sha256='304c9b202ea6fbd0a4a8e0ad3733715fbd4749f2204a9173a58ec53c32ea73e8')
    version('2.7.13', sha256='a4f05a0720ce0fd92626f0278b6b433eee9a6173ddf2bced7957dfb599a5ece1')
    version('2.7.12', sha256='3cb522d17463dfa69a155ab18cffa399b358c966c0363d6c8b5b3bf1384da4b6')
    version('2.7.11', sha256='82929b96fd6afc8da838b149107078c02fa1744b7e60999a8babbc0d3fa86fc6')
    version('2.7.10', sha256='eda8ce6eec03e74991abb5384170e7c65fcd7522e409b8e83d7e6372add0f12a')
    version('2.7.9',  sha256='c8bba33e66ac3201dabdc556f0ea7cfe6ac11946ec32d357c4c6f9b018c12c5b')
    version('2.7.8',  sha256='74d70b914da4487aa1d97222b29e9554d042f825f26cb2b93abd20fdda56b557')

    extendable = True

    # Variants to avoid cyclical dependencies for concretizer
    variant('libxml2', default=True,
            description='Use a gettext library build with libxml2')

    variant(
        'debug', default=False,
        description="debug build with extra checks (this is high overhead)"
    )

    # --enable-shared is known to cause problems for some users on macOS
    # This is a problem for Python 2.7 only, not Python3
    # See http://bugs.python.org/issue29846
    variant('shared', default=True,
            description='Enable shared libraries')
    # From https://docs.python.org/2/c-api/unicode.html: Python's default
    # builds use a 16-bit type for Py_UNICODE and store Unicode values
    # internally as UCS2. It is also possible to build a UCS4 version of Python
    # (most recent Linux distributions come with UCS4 builds of Python).  These
    # builds then use a 32-bit type for Py_UNICODE and store Unicode data
    # internally as UCS4. Note that UCS2 and UCS4 Python builds are not binary
    # compatible.
    variant('ucs4', default=False,
            description='Enable UCS4 (wide) unicode strings')
    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')
    variant(
        'optimizations',
        default=False,
        description='Enable expensive build-time optimizations, if available'
    )
    # See https://legacy.python.org/dev/peps/pep-0394/
    variant('pythoncmd', default=True,
            description="Symlink 'python3' executable to 'python' "
            "(not PEP 394 compliant)")

    # Optional Python modules
    variant('readline', default=True,  description='Build readline module')
    variant('ssl',      default=True,  description='Build ssl module')
    variant('sqlite3',  default=True,  description='Build sqlite3 module')
    variant('dbm',      default=True,  description='Build dbm module')
    variant('nis',      default=False, description='Build nis module')
    variant('zlib',     default=True,  description='Build zlib module')
    variant('bz2',      default=True,  description='Build bz2 module')
    variant('lzma',     default=True,  description='Build lzma module')
    variant('pyexpat',  default=True,  description='Build pyexpat module')
    variant('ctypes',   default=True,  description='Build ctypes module')
    variant('tkinter',  default=False, description='Build tkinter module')
    variant('uuid',     default=True,  description='Build uuid module')
    variant('tix',      default=False, description='Build Tix module')

    depends_on('pkgconfig@0.9.0:', type='build')
    depends_on('gettext +libxml2', when='+libxml2')
    depends_on('gettext ~libxml2', when='~libxml2')

    # Optional dependencies
    # See detect_modules() in setup.py for details
    depends_on('readline', when='+readline')
    depends_on('ncurses', when='+readline')
    depends_on('openssl', when='+ssl')
    # https://raw.githubusercontent.com/python/cpython/84471935ed2f62b8c5758fd544c7d37076fe0fa5/Misc/NEWS
    # https://docs.python.org/3.5/whatsnew/changelog.html#python-3-5-4rc1
    depends_on('openssl@:1.0.2z', when='@:2.7.13,3.0.0:3.5.2+ssl')
    depends_on('openssl@1.0.2:', when='@3.7:+ssl')  # https://docs.python.org/3/whatsnew/3.7.html#build-changes
    depends_on('sqlite@3.0.8:', when='+sqlite3')
    depends_on('gdbm', when='+dbm')  # alternatively ndbm or berkeley-db
    depends_on('libnsl', when='+nis')
    depends_on('zlib@1.1.3:', when='+zlib')
    depends_on('bzip2', when='+bz2')
    depends_on('xz', when='@3.3:+lzma')
    depends_on('expat', when='+pyexpat')
    depends_on('libffi', when='+ctypes')
    depends_on('tk', when='+tkinter')
    depends_on('tcl', when='+tkinter')
    depends_on('tix', when='+tix')
    if sys.platform != 'darwin':
        # On macOS systems, Spack's libuuid conflicts with the system-installed
        # version and breaks anything linked against Cocoa/Carbon. Since the
        # system-provided version is sufficient to build Python's UUID support,
        # the easy solution is to only depend on Spack's libuuid when *not* on
        # a Mac.
        depends_on('libuuid', when='+uuid')

    # Python needs to be patched to build extensions w/ mixed C/C++ code:
    # https://github.com/NixOS/nixpkgs/pull/19585/files
    # https://bugs.python.org/issue1222585
    #
    # NOTE: This patch puts Spack's default Python installation out of
    # sync with standard Python installs. If you're using such an
    # installation as an external and encountering build issues with mixed
    # C/C++ modules, consider installing a Spack-managed Python with
    # this patch instead. For more information, see:
    # https://github.com/spack/spack/pull/16856
    patch('python-2.7.8-distutils-C++.patch', when='@2.7.8:2.7.16')
    patch('python-2.7.17+-distutils-C++.patch', when='@2.7.17:2.7.18')
    patch('python-3.6.8-distutils-C++.patch', when='@3.6.8,3.7.2')
    patch('python-3.7.3-distutils-C++.patch', when='@3.7.3')
    patch('python-3.7.4+-distutils-C++.patch', when='@3.7.4:')

    # TODO: There's currently no way to ignore the fact that a single module failed, even if the
    # variant corresponding to that module is deselected. These patches comment out sections of
    # setup.py, specifically for the purpose of python 2.6 compat.
    patch('no-ssl.patch', when='~ssl')
    patch('no-dbm.patch', when='~dbm')

    patch('tkinter.patch', when='@:2.8,3.3:3.7 platform=darwin')

    # Ensure that distutils chooses correct compiler option for RPATH on cray:
    patch('cray-rpath-2.3.patch', when='@2.3:3.0.1 platform=cray')
    patch('cray-rpath-3.1.patch', when='@3.1:3.99  platform=cray')

    # Ensure that distutils chooses correct compiler option for RPATH on fj:
    patch('fj-rpath-2.3.patch', when='@2.3:3.0.1 %fj')
    patch('fj-rpath-3.1.patch', when='@3.1:3.99  %fj')

    # Fixes an alignment problem with more aggressive optimization in gcc8
    # https://github.com/python/cpython/commit/0b91f8a668201fc58fa732b8acc496caedfdbae0
    patch('gcc-8-2.7.14.patch', when='@2.7.14 %gcc@8:')

    # Fixes build with the Intel compilers
    # https://github.com/python/cpython/pull/16717
    patch('intel-3.6.7.patch', when='@3.6.7:3.6.8,3.7.1:3.7.5 %intel')

    # CPython tries to build an Objective-C file with GCC's C frontend
    # https://github.com/spack/spack/pull/16222
    # https://github.com/python/cpython/pull/13306
    conflicts('%gcc platform=darwin',
              msg='CPython does not compile with GCC on macOS yet, use clang. '
                  'See: https://github.com/python/cpython/pull/13306')
    # For more information refer to this bug report:
    # https://bugs.python.org/issue29712
    conflicts(
        '@:2.8 +shared',
        when='+optimizations',
        msg='+optimizations is incompatible with +shared in python@2.X'
    )
    conflicts('+tix', when='~tkinter',
              msg='python+tix requires python+tix+tkinter')

    conflicts('%nvhpc')

    _DISTUTIL_VARS_TO_SAVE = ['LDSHARED']
    _DISTUTIL_CACHE_FILENAME = 'sysconfig.json'
    _distutil_vars = None

    # Used to cache home locations, since computing them might be expensive
    _homes = {}

    # An in-source build with --enable-optimizations fails for python@3.X
    build_directory = 'spack-build'

    executables = [r'^python[\d.]*[mw]?$']

    @classmethod
    def determine_version(cls, exe):
        # Newer versions of Python support `--version`,
        # but older versions only support `-V`
        # Python 2 sends to STDERR, while Python 3 sends to STDOUT
        # Output looks like:
        #   Python 3.7.7
        output = Executable(exe)('-V', output=str, error=str)
        match = re.search(r'Python\s+(\S+)', output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version_str):
        python = Executable(exes[0])

        variants = ''
        for module in ['readline', 'sqlite3', 'dbm', 'nis',
                       'zlib', 'bz2', 'lzma', 'ctypes', 'uuid']:
            try:
                python('-c', 'import ' + module, error=os.devnull)
                variants += '+' + module
            except ProcessError:
                variants += '~' + module

        # Some variants enable multiple modules
        try:
            python('-c', 'import ssl', error=os.devnull)
            python('-c', 'import hashlib', error=os.devnull)
            variants += '+ssl'
        except ProcessError:
            variants += '~ssl'

        try:
            python('-c', 'import xml.parsers.expat', error=os.devnull)
            python('-c', 'import xml.etree.ElementTree', error=os.devnull)
            variants += '+pyexpat'
        except ProcessError:
            variants += '~pyexpat'

        # Some modules changed names in Python 3
        if Version(version_str) >= Version('3'):
            try:
                python('-c', 'import tkinter', error=os.devnull)
                variants += '+tkinter'
            except ProcessError:
                variants += '~tkinter'

            try:
                python('-c', 'import tkinter.tix', error=os.devnull)
                variants += '+tix'
            except ProcessError:
                variants += '~tix'
        else:
            try:
                python('-c', 'import Tkinter', error=os.devnull)
                variants += '+tkinter'
            except ProcessError:
                variants += '~tkinter'

            try:
                python('-c', 'import Tix', error=os.devnull)
                variants += '+tix'
            except ProcessError:
                variants += '~tix'

        return variants

    def url_for_version(self, version):
        url = "https://www.python.org/ftp/python/{0}/Python-{1}.tgz"
        return url.format(re.split('[a-z]', str(version))[0], version)

    # TODO: Ideally, these patches would be applied as separate '@run_before'
    # functions enabled via '@when', but these two decorators don't work
    # when used together. See: https://github.com/spack/spack/issues/12736
    def patch(self):
        # NOTE: Python's default installation procedure makes it possible for a
        # user's local configurations to change the Spack installation.  In
        # order to prevent this behavior for a full installation, we must
        # modify the installation script so that it ignores user files.
        if self.spec.satisfies('@2.7:2.8,3.4:'):
            ff = FileFilter('Makefile.pre.in')
            ff.filter(
                r'^(.*)setup\.py(.*)((build)|(install))(.*)$',
                r'\1setup.py\2 --no-user-cfg \3\6'
            )

        # NOTE: Older versions of Python do not support the '--with-openssl'
        # configuration option, so the installation's module setup file needs
        # to be modified directly in order to point to the correct SSL path.
        # See: https://stackoverflow.com/a/5939170
        if self.spec.satisfies('@:3.6.999+ssl'):
            ff = FileFilter(join_path('Modules', 'Setup.dist'))
            ff.filter(r'^#(((SSL=)|(_ssl))(.*))$', r'\1')
            ff.filter(r'^#((.*)(\$\(SSL\))(.*))$', r'\1')
            ff.filter(
                r'^SSL=(.*)$',
                r'SSL={0}'.format(self.spec['openssl'].prefix)
            )
        # Because Python uses compiler system paths during install, it's
        # possible to pick up a system OpenSSL when building 'python~ssl'.
        # To avoid this scenario, we disable the 'ssl' module with patching.
        elif self.spec.satisfies('@:3.6.999~ssl'):
            ff = FileFilter('setup.py')
            ff.filter(
                r'^(\s+(ssl_((incs)|(libs)))\s+=\s+)(.*)$',
                r'\1 None and \6'
            )
            ff.filter(
                r'^(\s+(opensslv_h)\s+=\s+)(.*)$',
                r'\1 None and \3'
            )

    def setup_build_environment(self, env):
        spec = self.spec

        # TODO: Python has incomplete support for Python modules with mixed
        # C/C++ source, and patches are required to enable building for these
        # modules. All Python versions without a viable patch are installed
        # with a warning message about this potentially erroneous behavior.
        if not spec.satisfies('@2.7.8:2.7.18,3.6.8,3.7.2:'):
            tty.warn(('Python v{0} does not have the C++ "distutils" patch; '
                      'errors may occur when installing Python modules w/ '
                      'mixed C/C++ source files.').format(self.version))

        # Need this to allow python build to find the Python installation.
        env.set('MACOSX_DEPLOYMENT_TARGET', platform.mac_ver()[0])

        env.unset('PYTHONPATH')
        env.unset('PYTHONHOME')

        setup_libtirpc_build_environment(spec, env)

    def flag_handler(self, name, flags):
        # python 3.8 requires -fwrapv when compiled with intel
        if self.spec.satisfies('@3.8: %intel'):
            if name == 'cflags':
                flags.append('-fwrapv')

        # allow flags to be passed through compiler wrapper
        return (flags, None, None)

    def configure_args(self):
        spec = self.spec
        config_args = []

        # setup.py needs to be able to read the CPPFLAGS and LDFLAGS
        # as it scans for the library and headers to build
        link_deps = spec.dependencies('link')

        cppflags = []
        ldflags = []
        if link_deps:
            # Header files are often included assuming they reside in a
            # subdirectory of prefix.include, e.g. #include <openssl/ssl.h>,
            # which is why we don't use HeaderList here. The header files of
            # libffi reside in prefix.lib but the configure script of Python
            # finds them using pkg-config.
            cppflags.extend('-I' + spec[dep.name].prefix.include for dep in link_deps)

            # Currently, the only way to get SpecBuildInterface wrappers of the
            # dependencies (which we need to get their 'libs') is to get them
            # using spec.__getitem__.
            ldflags.extend(spec[dep.name].libs.ld_flags for dep in link_deps)

        config_args.extend([
            'CPPFLAGS=' + ' '.join(cppflags),
            'LDFLAGS=' + ' '.join(ldflags),
        ])

        # https://docs.python.org/3/whatsnew/3.7.html#build-changes
        if spec.satisfies('@:3.6'):
            config_args.append('--with-threads')

        if spec.satisfies('@2.7.13:2.8,3.5.3:', strict=True) \
                and '+optimizations' in spec:
            config_args.append('--enable-optimizations')

        if spec.satisfies('%gcc platform=darwin'):
            config_args.append('--disable-toolbox-glue')

        if spec.satisfies('%intel', strict=True) and \
                spec.satisfies('@2.7.12:2.8,3.5.2:', strict=True):
            config_args.append('--with-icc')

        if '+debug' in spec:
            config_args.append('--with-pydebug')
        else:
            config_args.append('--without-pydebug')

        if '+shared' in spec:
            config_args.append('--enable-shared')
        else:
            config_args.append('--disable-shared')

        if '+ucs4' in spec:
            if spec.satisfies('@:2.7'):
                config_args.append('--enable-unicode=ucs4')
            elif spec.satisfies('@3.0:3.2'):
                config_args.append('--with-wide-unicode')
            elif spec.satisfies('@3.3:'):
                # https://docs.python.org/3.3/whatsnew/3.3.html#functionality
                raise ValueError(
                    '+ucs4 variant not compatible with Python 3.3 and beyond')

        if spec.satisfies('@3:'):
            config_args.append('--without-ensurepip')

        if '+pic' in spec:
            config_args.append('CFLAGS={0}'.format(self.compiler.cc_pic_flag))

        if '+ssl' in spec:
            if spec.satisfies('@3.7:'):
                config_args.append('--with-openssl={0}'.format(
                    spec['openssl'].prefix))

        if '+dbm' in spec:
            # Default order is ndbm:gdbm:bdb
            config_args.append('--with-dbmliborder=gdbm:bdb:ndbm')
        else:
            config_args.append('--with-dbmliborder=')

        if '+pyexpat' in spec:
            config_args.append('--with-system-expat')
        else:
            config_args.append('--without-system-expat')

        if '+ctypes' in spec:
            config_args.append('--with-system-ffi')
        else:
            config_args.append('--without-system-ffi')

        if '+tkinter' in spec:
            config_args.extend([
                '--with-tcltk-includes=-I{0} -I{1}'.format(
                    spec['tcl'].prefix.include, spec['tk'].prefix.include),
                '--with-tcltk-libs={0} {1}'.format(
                    spec['tcl'].libs.ld_flags, spec['tk'].libs.ld_flags)
            ])

        # https://docs.python.org/3.8/library/sqlite3.html#f1
        if spec.satisfies('@3.2: +sqlite3'):
            config_args.append('--enable-loadable-sqlite-extensions')

        return config_args

    @run_after('install')
    def _save_distutil_vars(self):
        """
        Run before changing automatically generated contents of the
        _sysconfigdata.py, which is used by distutils to figure out what
        executables to use while compiling and linking extensions. If we build
        extensions with spack those executables should be spack's wrappers.
        Spack partially covers this by setting environment variables that
        are also accounted for by distutils. Currently there is one more known
        variable that must be set, which is LDSHARED, so the method saves its
        autogenerated value to pass it to the dependent package's setup script.
        """

        self._distutil_vars = {}

        input_filename = self.get_sysconfigdata_name()
        input_dict = None
        try:
            with open(input_filename) as input_file:
                match = re.search(r'build_time_vars\s*=\s*(?P<dict>{.*})',
                                  input_file.read(),
                                  flags=re.DOTALL)

                if match:
                    input_dict = ast.literal_eval(match.group('dict'))
        except (IOError, SyntaxError):
            pass

        if not input_dict:
            tty.warn("Failed to find 'build_time_vars' dictionary in file "
                     "'%s'. This might cause the extensions that are "
                     "installed with distutils to call compilers directly "
                     "avoiding Spack's wrappers." % input_filename)
            return

        for var_name in Python._DISTUTIL_VARS_TO_SAVE:
            if var_name in input_dict:
                self._distutil_vars[var_name] = input_dict[var_name]
            else:
                tty.warn("Failed to find key '%s' in 'build_time_vars' "
                         "dictionary in file '%s'. This might cause the "
                         "extensions that are installed with distutils to "
                         "call compilers directly avoiding Spack's wrappers."
                         % (var_name, input_filename))

        if len(self._distutil_vars) > 0:
            output_filename = None
            try:
                output_filename = join_path(
                    spack.store.layout.metadata_path(self.spec),
                    Python._DISTUTIL_CACHE_FILENAME)
                with open(output_filename, 'w') as output_file:
                    sjson.dump(self._distutil_vars, output_file)
            except Exception:
                tty.warn("Failed to save metadata for distutils. This might "
                         "cause the extensions that are installed with "
                         "distutils to call compilers directly avoiding "
                         "Spack's wrappers.")
                # We make the cache empty if we failed to save it to file
                # to provide the same behaviour as in the case when the cache
                # is initialized by the method load_distutils_data().
                self._distutil_vars = {}
                if output_filename:
                    force_remove(output_filename)

    def _load_distutil_vars(self):
        # We update and keep the cache unchanged only if the package is
        # installed.
        if not self._distutil_vars and self.installed:
            try:
                input_filename = join_path(
                    spack.store.layout.metadata_path(self.spec),
                    Python._DISTUTIL_CACHE_FILENAME)
                if os.path.isfile(input_filename):
                    with open(input_filename) as input_file:
                        self._distutil_vars = sjson.load(input_file)
            except Exception:
                pass

            if not self._distutil_vars:
                self._distutil_vars = {}

        return self._distutil_vars

    @run_after('install')
    def filter_compilers(self):
        """Run after install to tell the configuration files and Makefiles
        to use the compilers that Spack built the package with.

        If this isn't done, they'll have CC and CXX set to Spack's generic
        cc and c++. We want them to be bound to whatever compiler
        they were built with."""

        kwargs = {'ignore_absent': True, 'backup': False, 'string': True}

        filenames = [
            self.get_sysconfigdata_name(), self.get_makefile_filename()
        ]

        filter_file(spack_cc,  self.compiler.cc,  *filenames, **kwargs)
        if spack_cxx and self.compiler.cxx:
            filter_file(spack_cxx, self.compiler.cxx, *filenames, **kwargs)

    @run_after('install')
    def symlink(self):
        spec = self.spec
        prefix = self.prefix

        # TODO:
        # On OpenSuse 13, python uses <prefix>/lib64/python2.7/lib-dynload/*.so
        # instead of <prefix>/lib/python2.7/lib-dynload/*.so. Oddly enough the
        # result is that Python can not find modules like cPickle. A workaround
        # for now is to symlink to `lib`:
        src = os.path.join(prefix.lib64,
                           'python{0}'.format(self.version.up_to(2)),
                           'lib-dynload')
        dst = os.path.join(prefix.lib,
                           'python{0}'.format(self.version.up_to(2)),
                           'lib-dynload')
        if os.path.isdir(src) and not os.path.isdir(dst):
            mkdirp(dst)
            for f in os.listdir(src):
                os.symlink(os.path.join(src, f),
                           os.path.join(dst, f))

        if spec.satisfies('@3:') and spec.satisfies('+pythoncmd'):
            os.symlink(os.path.join(prefix.bin, 'python3'),
                       os.path.join(prefix.bin, 'python'))
            os.symlink(os.path.join(prefix.bin, 'python3-config'),
                       os.path.join(prefix.bin, 'python-config'))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def import_tests(self):
        """Test that basic Python functionality works."""

        spec = self.spec

        with working_dir('spack-test', create=True):
            # Ensure that readline module works
            if '+readline' in spec:
                self.command('-c', 'import readline')

            # Ensure that ssl module works
            if '+ssl' in spec:
                self.command('-c', 'import ssl')
                self.command('-c', 'import hashlib')

            # Ensure that sqlite3 module works
            if '+sqlite3' in spec:
                self.command('-c', 'import sqlite3')

            # Ensure that dbm module works
            if '+dbm' in spec:
                self.command('-c', 'import dbm')

            # Ensure that nis module works
            if '+nis' in spec:
                self.command('-c', 'import nis')

            # Ensure that zlib module works
            if '+zlib' in spec:
                self.command('-c', 'import zlib')

            # Ensure that bz2 module works
            if '+bz2' in spec:
                self.command('-c', 'import bz2')

            # Ensure that lzma module works
            if spec.satisfies('@3.3:'):
                if '+lzma' in spec:
                    self.command('-c', 'import lzma')

            # Ensure that pyexpat module works
            if '+pyexpat' in spec:
                self.command('-c', 'import xml.parsers.expat')
                self.command('-c', 'import xml.etree.ElementTree')

            # Ensure that ctypes module works
            if '+ctypes' in spec:
                self.command('-c', 'import ctypes')

            # Ensure that tkinter module works
            # https://wiki.python.org/moin/TkInter
            if '+tkinter' in spec:
                # Only works if ForwardX11Trusted is enabled, i.e. `ssh -Y`
                if 'DISPLAY' in env:
                    if spec.satisfies('@3:'):
                        self.command('-c', 'import tkinter; tkinter._test()')
                    else:
                        self.command('-c', 'import Tkinter; Tkinter._test()')
                else:
                    if spec.satisfies('@3:'):
                        self.command('-c', 'import tkinter')
                    else:
                        self.command('-c', 'import Tkinter')

            # Ensure that uuid module works
            if '+uuid' in spec:
                self.command('-c', 'import uuid')

            # Ensure that tix module works
            if '+tix' in spec:
                if spec.satisfies('@3:'):
                    self.command('-c', 'import tkinter.tix')
                else:
                    self.command('-c', 'import Tix')

    # ========================================================================
    # Set up environment to make install easy for python extensions.
    # ========================================================================

    @property
    def command(self):
        """Returns the Python command, which may vary depending
        on the version of Python and how it was installed.

        In general, Python 2 comes with ``python`` and ``python2`` commands,
        while Python 3 only comes with a ``python3`` command. However, some
        package managers will symlink ``python`` to ``python3``, while others
        may contain ``python3.6``, ``python3.5``, and ``python3.4`` in the
        same directory.

        Returns:
            Executable: the Python command
        """
        # We need to be careful here. If the user is using an externally
        # installed python, several different commands could be located
        # in the same directory. Be as specific as possible. Search for:
        #
        # * python3.6
        # * python3
        # * python
        #
        # in that order if using python@3.6.5, for example.
        version = self.spec.version
        for ver in [version.up_to(2), version.up_to(1), '']:
            path = os.path.join(self.prefix.bin, 'python{0}'.format(ver))
            if os.path.exists(path):
                return Executable(path)
        else:
            msg = 'Unable to locate {0} command in {1}'
            raise RuntimeError(msg.format(self.name, self.prefix.bin))

    def print_string(self, string):
        """Returns the appropriate print string depending on the
        version of Python.

        Examples:

        * Python 2

          .. code-block:: python

             >>> self.print_string('sys.prefix')
             'print sys.prefix'

        * Python 3

          .. code-block:: python

             >>> self.print_string('sys.prefix')
             'print(sys.prefix)'
        """
        if self.spec.satisfies('@:2'):
            return 'print {0}'.format(string)
        else:
            return 'print({0})'.format(string)

    def get_config_var(self, key):
        """Return the value of a single variable. Wrapper around
        ``distutils.sysconfig.get_config_var()``."""

        cmd = 'from distutils.sysconfig import get_config_var; '
        cmd += self.print_string("get_config_var('{0}')".format(key))

        return self.command('-c', cmd, output=str).strip()

    def get_config_h_filename(self):
        """Return the full path name of the configuration header.
        Wrapper around ``distutils.sysconfig.get_config_h_filename()``."""

        cmd = 'from distutils.sysconfig import get_config_h_filename; '
        cmd += self.print_string('get_config_h_filename()')

        return self.command('-c', cmd, output=str).strip()

    def get_makefile_filename(self):
        """Return the full path name of ``Makefile`` used to build Python.
        Wrapper around ``distutils.sysconfig.get_makefile_filename()``."""

        cmd = 'from distutils.sysconfig import get_makefile_filename; '
        cmd += self.print_string('get_makefile_filename()')

        return self.command('-c', cmd, output=str).strip()

    def get_python_inc(self):
        """Return the directory for either the general or platform-dependent C
        include files. Wrapper around ``distutils.sysconfig.get_python_inc()``.
        """

        cmd = 'from distutils.sysconfig import get_python_inc; '
        cmd += self.print_string('get_python_inc()')

        return self.command('-c', cmd, output=str).strip()

    def get_python_lib(self):
        """Return the directory for either the general or platform-dependent
        library installation. Wrapper around
        ``distutils.sysconfig.get_python_lib()``."""

        cmd = 'from distutils.sysconfig import get_python_lib; '
        cmd += self.print_string('get_python_lib()')

        return self.command('-c', cmd, output=str).strip()

    def get_sysconfigdata_name(self):
        """Return the full path name of the sysconfigdata file."""

        libdest = self.get_config_var('LIBDEST')

        filename = '_sysconfigdata.py'
        if self.spec.satisfies('@3.6:'):
            # Python 3.6.0 renamed the sys config file
            cmd = 'from sysconfig import _get_sysconfigdata_name; '
            cmd += self.print_string('_get_sysconfigdata_name()')
            filename = self.command('-c', cmd, output=str).strip()
            filename += '.py'

        return join_path(libdest, filename)

    @property
    def home(self):
        """Most of the time, ``PYTHONHOME`` is simply
        ``spec['python'].prefix``. However, if the user is using an
        externally installed python, it may be symlinked. For example,
        Homebrew installs python in ``/usr/local/Cellar/python/2.7.12_2``
        and symlinks it to ``/usr/local``. Users may not know the actual
        installation directory and add ``/usr/local`` to their
        ``packages.yaml`` unknowingly. Query the python executable to
        determine exactly where it is installed. Fall back on
        ``spec['python'].prefix`` if that doesn't work."""

        dag_hash = self.spec.dag_hash()
        if dag_hash not in self._homes:
            try:
                prefix = self.get_config_var('prefix')
            except ProcessError:
                prefix = self.prefix
            self._homes[dag_hash] = Prefix(prefix)
        return self._homes[dag_hash]

    @property
    def libs(self):
        # Spack installs libraries into lib, except on openSUSE where it
        # installs them into lib64. If the user is using an externally
        # installed package, it may be in either lib or lib64, so we need
        # to ask Python where its LIBDIR is.
        libdir = self.get_config_var('LIBDIR')

        # In Ubuntu 16.04.6 and python 2.7.12 from the system, lib could be
        # in LBPL
        # https://mail.python.org/pipermail/python-dev/2013-April/125733.html
        libpl = self.get_config_var('LIBPL')

        # The system Python installation on macOS and Homebrew installations
        # install libraries into a Frameworks directory
        frameworkprefix = self.get_config_var('PYTHONFRAMEWORKPREFIX')

        if '+shared' in self.spec:
            ldlibrary = self.get_config_var('LDLIBRARY')

            if os.path.exists(os.path.join(libdir, ldlibrary)):
                return LibraryList(os.path.join(libdir, ldlibrary))
            elif os.path.exists(os.path.join(libpl, ldlibrary)):
                return LibraryList(os.path.join(libpl, ldlibrary))
            elif os.path.exists(os.path.join(frameworkprefix, ldlibrary)):
                return LibraryList(os.path.join(frameworkprefix, ldlibrary))
            else:
                msg = 'Unable to locate {0} libraries in {1}'
                raise RuntimeError(msg.format(ldlibrary, libdir))
        else:
            library = self.get_config_var('LIBRARY')

            if os.path.exists(os.path.join(libdir, library)):
                return LibraryList(os.path.join(libdir, library))
            elif os.path.exists(os.path.join(frameworkprefix, library)):
                return LibraryList(os.path.join(frameworkprefix, library))
            else:
                msg = 'Unable to locate {0} libraries in {1}'
                raise RuntimeError(msg.format(library, libdir))

    @property
    def headers(self):
        try:
            config_h = self.get_config_h_filename()

            if not os.path.exists(config_h):
                includepy = self.get_config_var('INCLUDEPY')
                msg = 'Unable to locate {0} headers in {1}'
                raise RuntimeError(msg.format(self.name, includepy))

            headers = HeaderList(config_h)
        except ProcessError:
            headers = find_headers(
                'pyconfig', self.prefix.include, recursive=True)
            config_h = headers[0]

        headers.directories = [os.path.dirname(config_h)]
        return headers

    @property
    def python_lib_dir(self):
        return join_path('lib', 'python{0}'.format(self.version.up_to(2)))

    @property
    def python_include_dir(self):
        return join_path('include', 'python{0}'.format(self.version.up_to(2)))

    @property
    def site_packages_dir(self):
        return join_path(self.python_lib_dir, 'site-packages')

    @property
    def easy_install_file(self):
        return join_path(self.site_packages_dir, "easy-install.pth")

    def setup_run_environment(self, env):
        env.prepend_path('CPATH', os.pathsep.join(
            self.spec['python'].headers.directories))

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Set PYTHONPATH to include the site-packages directory for the
        extension and any other python extensions it depends on."""

        # If we set PYTHONHOME, we must also ensure that the corresponding
        # python is found in the build environment. This to prevent cases
        # where a system provided python is run against the standard libraries
        # of a Spack built python. See issue #7128
        env.set('PYTHONHOME', self.home)

        path = os.path.dirname(self.command.path)
        if not is_system_path(path):
            env.prepend_path('PATH', path)

        python_paths = []
        for d in dependent_spec.traverse(deptype=('build', 'run', 'test')):
            if d.package.extends(self.spec):
                # Python libraries may be installed in lib or lib64
                # See issues #18520 and #17126
                for lib in ['lib', 'lib64']:
                    python_paths.append(join_path(
                        d.prefix, lib, 'python' + str(self.version.up_to(2)),
                        'site-packages'))

        pythonpath = ':'.join(python_paths)
        env.set('PYTHONPATH', pythonpath)

    def setup_dependent_run_environment(self, env, dependent_spec):
        python_paths = []
        for d in dependent_spec.traverse(deptype='run'):
            if d.package.extends(self.spec):
                # Python libraries may be installed in lib or lib64
                # See issues #18520 and #17126
                for lib in ['lib', 'lib64']:
                    root = join_path(
                        d.prefix, lib, 'python' + str(self.version.up_to(2)),
                        'site-packages')
                    if os.path.exists(root):
                        python_paths.append(root)

        pythonpath = ':'.join(python_paths)
        env.prepend_path('PYTHONPATH', pythonpath)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before python modules' install() methods.

        In most cases, extensions will only need to have one line::

        setup_py('install', '--prefix={0}'.format(prefix))"""

        module.python = self.command

        if self.version.up_to(2).string == '2.6':
            trailing_args = []
        else:
            trailing_args = ['--no-user-cfg']
        args = ['setup.py', *tuple(trailing_args)]
        full_cmdline = self.command.path + ' {0}'.format(' '.join(args))
        module.setup_py = Executable(full_cmdline)

        distutil_vars = self._load_distutil_vars()

        if distutil_vars:
            for key, value in distutil_vars.items():
                module.setup_py.add_default_env(key, value)

        # Add variables for lib/pythonX.Y and lib/pythonX.Y/site-packages dirs.
        module.python_lib_dir = join_path(dependent_spec.prefix,
                                          self.python_lib_dir)
        module.python_include_dir = join_path(dependent_spec.prefix,
                                              self.python_include_dir)
        module.site_packages_dir = join_path(dependent_spec.prefix,
                                             self.site_packages_dir)

        self.spec.home = self.home

        # Make the site packages directory for extensions
        if dependent_spec.package.is_extension:
            mkdirp(module.site_packages_dir)

    # ========================================================================
    # Handle specifics of activating and deactivating python modules.
    # ========================================================================

    def python_ignore(self, ext_pkg, args):
        """Add some ignore files to activate/deactivate args."""
        ignore_arg = args.get('ignore', lambda f: False)

        # Always ignore easy-install.pth, as it needs to be merged.
        patterns = [r'site-packages/easy-install\.pth$']

        # Ignore pieces of setuptools installed by other packages.
        # Must include directory name or it will remove all site*.py files.
        if ext_pkg.name != 'py-setuptools':
            patterns.extend([
                r'bin/easy_install[^/]*$',
                r'site-packages/setuptools[^/]*\.egg$',
                r'site-packages/setuptools\.pth$',
                r'site-packages/site[^/]*\.pyc?$',
                r'site-packages/__pycache__/site[^/]*\.pyc?$'
            ])
        if ext_pkg.name != 'py-pygments':
            patterns.append(r'bin/pygmentize$')
        if ext_pkg.name != 'py-numpy':
            patterns.append(r'bin/f2py[0-9.]*$')

        return match_predicate(ignore_arg, patterns)

    def write_easy_install_pth(self, exts, prefix=None):
        if not prefix:
            prefix = self.prefix

        paths = []
        unique_paths = set()

        for ext in sorted(exts.values()):
            easy_pth = join_path(ext.prefix, self.easy_install_file)

            if not os.path.isfile(easy_pth):
                continue

            with open(easy_pth) as f:
                for line in f:
                    line = line.rstrip()

                    # Skip lines matching these criteria
                    if not line:
                        continue
                    if re.search(r'^(import|#)', line):
                        continue
                    if (ext.name != 'py-setuptools' and
                            re.search(r'setuptools.*egg$', line)):
                        continue

                    if line not in unique_paths:
                        unique_paths.add(line)
                        paths.append(line)

        main_pth = join_path(prefix, self.easy_install_file)

        if not paths:
            if os.path.isfile(main_pth):
                os.remove(main_pth)

        else:
            with open(main_pth, 'w') as f:
                f.write("import sys; sys.__plen = len(sys.path)\n")
                for path in paths:
                    f.write("{0}\n".format(path))
                f.write("import sys; new=sys.path[sys.__plen:]; "
                        "del sys.path[sys.__plen:]; "
                        "p=getattr(sys,'__egginsert',0); "
                        "sys.path[p:p]=new; "
                        "sys.__egginsert = p+len(new)\n")

    def activate(self, ext_pkg, view, **args):
        ignore = self.python_ignore(ext_pkg, args)
        args.update(ignore=ignore)

        super(Python, self).activate(ext_pkg, view, **args)

        extensions_layout = view.extensions_layout
        exts = extensions_layout.extension_map(self.spec)
        exts[ext_pkg.name] = ext_pkg.spec

        self.write_easy_install_pth(exts, prefix=view.get_projection_for_spec(
            self.spec
        ))

    def deactivate(self, ext_pkg, view, **args):
        args.update(ignore=self.python_ignore(ext_pkg, args))

        super(Python, self).deactivate(ext_pkg, view, **args)

        extensions_layout = view.extensions_layout
        exts = extensions_layout.extension_map(self.spec)
        # Make deactivate idempotent
        if ext_pkg.name in exts:
            del exts[ext_pkg.name]
            self.write_easy_install_pth(exts,
                                        prefix=view.get_projection_for_spec(
                                            self.spec
                                        ))

    def add_files_to_view(self, view, merge_map):
        bin_dir = self.spec.prefix.bin
        for src, dst in merge_map.items():
            if not path_contains_subdirectory(src, bin_dir):
                view.link(src, dst, spec=self.spec)
            elif not os.path.islink(src):
                copy(src, dst)
                if 'script' in get_filetype(src):
                    filter_file(
                        self.spec.prefix,
                        os.path.abspath(
                            view.get_projection_for_spec(self.spec)
                        ),
                        dst,
                        backup=False
                    )
            else:
                # orig_link_target = os.path.realpath(src) is insufficient when
                # the spack install tree is located at a symlink or a
                # descendent of a symlink. What we need here is the real
                # relative path from the python prefix to src
                # TODO: generalize this logic in the link_tree object
                #    add a method to resolve a link relative to the link_tree
                #    object root.
                realpath_src = os.path.realpath(src)
                realpath_prefix = os.path.realpath(self.spec.prefix)
                realpath_rel = os.path.relpath(realpath_src, realpath_prefix)
                orig_link_target = os.path.join(self.spec.prefix, realpath_rel)

                new_link_target = os.path.abspath(merge_map[orig_link_target])
                view.link(new_link_target, dst, spec=self.spec)

    def remove_files_from_view(self, view, merge_map):
        bin_dir = self.spec.prefix.bin
        for src, dst in merge_map.items():
            if not path_contains_subdirectory(src, bin_dir):
                view.remove_file(src, dst)
            else:
                os.remove(dst)

    def test(self):
        # do not use self.command because we are also testing the run env
        exe = self.spec['python'].command.name

        # test hello world
        msg = 'hello world!'
        reason = 'test: running {0}'.format(msg)
        options = ['-c', 'print("{0}")'.format(msg)]
        self.run_test(exe, options=options, expected=[msg], installed=True,
                      purpose=reason)

        # checks import works and executable comes from the spec prefix
        reason = 'test: checking import and executable'
        print_str = self.print_string('sys.executable')
        options = ['-c', 'import sys; {0}'.format(print_str)]
        self.run_test(exe, options=options, expected=[self.spec.prefix],
                      installed=True, purpose=reason)
