# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class FluxCore(AutotoolsPackage):
    """ A next-generation resource manager (pre-alpha) """

    homepage = "https://github.com/flux-framework/flux-core"
    url      = "https://github.com/flux-framework/flux-core/releases/download/v0.8.0/flux-core-0.8.0.tar.gz"
    git      = "https://github.com/flux-framework/flux-core.git"
    maintainers = ['SteVwonder']

    version('master', branch='master')
    version('0.23.0', sha256='918b181be4e27c32f02d5036230212cd9235dc78dc2bde249c3651d6f75866c7')
    version('0.22.0', sha256='1dd0b737199b8a40f245e6a4e1b3b28770f0ecf2f483d284232080b8b252521f')
    version('0.21.0', sha256='cc1b7a46d7c1c1a3e99e8861bba0dde89a97351eabd6f1b264788bd76e64c329')
    version('0.20.0', sha256='2970b9b1c389fc4a381f9e605921ce0eb6aa9339387ea741978bcffb4bd81b6f')
    version('0.19.0', sha256='f45328a37d989c308c46639a9ed771f47b11184422cf5604249919fbd320d6f5')
    version('0.18.0', sha256='9784bbca94177a32dbbc99728e8925bf894f3aebaa316961d6ea85df32d59545')
    version('0.17.0', sha256='3f8c6cb72982028f86a96c0098cacd3a6e9de359fa1cf077380c835a20e7b7f7')
    version('0.16.0', sha256='1582f7fb4d2313127418c34de7c9ce4f5fef00622d19cedca7bed929f4709f10')
    version('0.15.0', sha256='51bc2eae69501f802459fc82f191eb5e8ae0b4f7e9e77ac18543a850cc8445f5')

    # Avoid the infinite symlink issue
    # This workaround is documented in PR #3543
    build_directory = 'spack-build'

    variant('docs', default=False, description='Build flux manpages')
    variant('cuda', default=False, description='Build dependencies with support for CUDA')

    depends_on("libzmq@4.0.4:")
    depends_on("czmq@3.0.1:")
    depends_on("hwloc@1.11.1:1.99", when="@:0.17.0")
    depends_on("hwloc@1.11.1:", when="@0.17.0:")
    depends_on("hwloc +cuda", when='+cuda')
    # Provide version hints for lua so that the concretizer succeeds when no
    # explicit flux-core version is given. See issue #10000 for details
    depends_on("lua", type=('build', 'run', 'link'))
    depends_on("lua@5.1:5.2.99", when="@:0.17.0")
    depends_on("lua@5.1:5.3.99", when="@0.18.0:,master")
    depends_on("lua-luaposix")
    # `link` dependency on python due to Flux's `pymod` module
    depends_on("python@3.6:", type=('build', 'run', 'link'))
    depends_on("py-cffi", type=('build', 'run'))
    depends_on("py-six", type=('build', 'run'))
    depends_on("py-pyyaml")
    depends_on("py-jsonschema")
    depends_on("jansson")
    depends_on("pkgconfig")
    depends_on("yaml-cpp")
    depends_on("lz4")

    depends_on("asciidoc", type='build', when="+docs")

    # Need autotools when building on master:
    depends_on("autoconf", type='build', when='@master')
    depends_on("automake", type='build', when='@master')
    depends_on("libtool", type='build', when='@master')

    # Testing Dependencies
    depends_on("mpich pmi=pmi", type="test")
    depends_on("valgrind", type="test")
    depends_on("jq", type="test")

    def url_for_version(self, version):
        '''
        Flux uses a fork of ZeroMQ's Collective Code Construction Contract
        (https://github.com/flux-framework/rfc/blob/master/spec_1.adoc).
        This model requires a repository fork for every stable release that has
        patch releases.  For example, 0.8.0 and 0.9.0 are both tags within the
        main repository, but 0.8.1 and 0.9.5 would be releases on the v0.8 and
        v0.9 forks, respectively.

        Rather than provide an explicit URL for each patch release, make Spack
        aware of this repo structure.
        '''
        if version[-1] == 0:
            url = "https://github.com/flux-framework/flux-core/releases/download/v{0}/flux-core-{0}.tar.gz"
        else:
            url = "https://github.com/flux-framework/flux-core-v{1}/releases/download/v{0}/flux-core-{0}.tar.gz"
        return url.format(version.up_to(3), version.up_to(2))

    def setup(self):
        pass

    @when('@master')
    def setup(self):
        with working_dir(self.stage.source_path):
            # Allow git-describe to get last tag so flux-version works:
            git = which('git')
            git('fetch', '--unshallow')
            git("config", "remote.origin.fetch",
                "+refs/heads/*:refs/remotes/origin/*")
            git('fetch', 'origin')

    def autoreconf(self, spec, prefix):
        self.setup()
        if not os.path.exists('configure'):
            # Bootstrap with autotools
            bash = which('bash')
            bash('./autogen.sh')

    @property
    def lua_version(self):
        return self.spec['lua'].version.up_to(2)

    @property
    def lua_share_dir(self):
        return os.path.join('share', 'lua', str(self.lua_version))

    @property
    def lua_lib_dir(self):
        return os.path.join('lib', 'lua', str(self.lua_version))

    def setup_build_environment(self, env):
        #  Ensure ./fluxometer.lua can be found during flux's make check
        env.append_path('LUA_PATH', './?.lua', separator=';')

    def setup_run_environment(self, env):
        env.prepend_path(
            'LUA_PATH',
            os.path.join(self.spec.prefix, self.lua_share_dir, '?.lua'),
            separator=';')
        env.prepend_path(
            'LUA_CPATH',
            os.path.join(self.spec.prefix, self.lua_lib_dir, '?.so'),
            separator=';')
        env.prepend_path(
            'PYTHONPATH',
            os.path.join(
                self.spec.prefix.lib,
                "python{0}".format(self.spec['python'].version.up_to(2)),
                "site-packages"),
        )
        env.prepend_path('FLUX_MODULE_PATH', self.prefix.lib.flux.modules)
        env.prepend_path('FLUX_EXEC_PATH', self.prefix.libexec.flux.cmd)
        env.prepend_path('FLUX_RC_PATH', self.prefix.etc.flux)
        env.prepend_path('FLUX_RC1_PATH', self.prefix.etc.flux.rc1)
        env.prepend_path('FLUX_RC3_PATH', self.prefix.etc.flux.rc3)
        env.prepend_path(
            'FLUX_CONNECTOR_PATH',
            self.prefix.lib.flux.connectors
        )
        env.prepend_path(
            'FLUX_PMI_LIBRARY_PATH',
            os.path.join(self.prefix.lib.flux, "libpmi.so")
        )
        # Wreck was removed in 0.12
        if self.version < Version("0.12.0"):
            env.prepend_path(
                'FLUX_WREXECD_PATH',
                self.prefix.libexec.flux.wrexecd
            )
            env.prepend_path(
                'FLUX_WRECK_LUA_PATTERN',
                os.path.join(self.prefix.etc.wreck, "lua.d", "*.lua")
            )

    def configure_args(self):
        args = ['--enable-pylint=no']
        if '+docs' not in self.spec:
            args.append('--disable-docs')
        return args

    def flag_handler(self, name, flags):
        if name == 'cflags':
            # https://github.com/flux-framework/flux-core/issues/3482
            if self.spec.satisfies('%gcc@10:') and \
               self.spec.satisfies('@0.23.0:0.23.99'):
                if flags is None:
                    flags = []
                flags.append('-Wno-error=stringop-truncation')

            if self.spec.satisfies('%gcc@8:') and \
               self.spec.satisfies('@0.23.0'):
                if flags is None:
                    flags = []
                flags.append('-Wno-error=maybe-uninitialized')

        return (flags, None, None)
