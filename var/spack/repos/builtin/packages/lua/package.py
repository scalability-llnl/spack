# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util.filesystem import join_path
from spack import *
import os


class Lua(Package):
    """The Lua programming language interpreter and library."""

    homepage = "http://www.lua.org"
    url = "http://www.lua.org/ftp/lua-5.3.4.tar.gz"

    version('5.3.5', sha256='0c2eed3f960446e1a3e4b9a1ca2f3ff893b6ce41942cf54d5dd59ab4b3b058ac')
    version('5.3.4', sha256='f681aa518233bc407e23acf0f5887c884f17436f000d453b2491a9f11a52400c')
    version('5.3.2', sha256='c740c7bb23a936944e1cc63b7c3c5351a8976d7867c5252c8854f7b2af9da68f')
    version('5.3.1', sha256='072767aad6cc2e62044a66e8562f51770d941e972dc1e4068ba719cd8bffac17')
    version('5.3.0', sha256='ae4a5eb2d660515eb191bfe3e061f2b8ffe94dce73d32cfd0de090ddcc0ddb01')
    version('5.2.4', sha256='b9e2e4aad6789b3b63a056d442f7b39f0ecfca3ae0f1fc0ae4e9614401b69f4b')
    version('5.2.3', sha256='13c2fb97961381f7d06d5b5cea55b743c163800896fd5c5e2356201d3619002d')
    version('5.2.2', sha256='3fd67de3f5ed133bf312906082fa524545c6b9e1b952e8215ffbd27113f49f00')
    version('5.2.1', sha256='64304da87976133196f9e4c15250b70f444467b6ed80d7cfd7b3b982b5177be5')
    version('5.2.0', sha256='cabe379465aa8e388988073d59b69e76ba0025429d2c1da80821a252cdf6be0d')
    version('5.1.5', sha256='2640fc56a795f29d28ef15e13c34a47e223960b0240e8cb0a82d9b0738695333')
    version('5.1.4', sha256='b038e225eaf2a5b57c9bcc35cd13aa8c6c8288ef493d52970c9545074098af3a')
    version('5.1.3', sha256='6b5df2edaa5e02bf1a2d85e1442b2e329493b30b0c0780f77199d24f087d296d')

    variant("pcfile", default=False, description="Add patch for lua.pc generation")
    variant('shared', default=True,
            description='Builds a shared version of the library')

    extendable = True

    depends_on('ncurses+termlib')
    depends_on('readline')
    # luarocks needs unzip for some packages (e.g. lua-luaposix)
    depends_on('unzip', type='run')

    patch(
        "http://lua.2524044.n2.nabble.com/attachment/7666421/0/pkg-config.patch",
        sha256="208316c2564bdd5343fa522f3b230d84bd164058957059838df7df56876cb4ae",
        when="+pcfile"
    )

    resource(
        name="luarocks",
        url="https://keplerproject.github.io/luarocks/releases/"
        "luarocks-2.3.0.tar.gz",
        sha256="68e38feeb66052e29ad1935a71b875194ed8b9c67c2223af5f4d4e3e2464ed97",
        destination="luarocks",
        placement='luarocks')

    def install(self, spec, prefix):
        if spec.satisfies("platform=darwin"):
            target = 'macosx'
        else:
            target = 'linux'
        make('INSTALL_TOP=%s' % prefix,
             'MYLDFLAGS=-L%s -L%s' % (
                 spec['readline'].prefix.lib,
                 spec['ncurses'].prefix.lib),
             'MYLIBS=-lncursesw -ltinfow',
             'CC=%s -std=gnu99 %s' % (spack_cc,
                                      self.compiler.cc_pic_flag),
             target)
        make('INSTALL_TOP=%s' % prefix,
             'install')

        if '+shared' in spec:
            static_to_shared_library(join_path(prefix.lib, 'liblua.a'),
                                     arguments=['-lm', '-ldl'],
                                     version=self.version,
                                     compat_version=self.version.up_to(2))

        # compatibility with ax_lua.m4 from autoconf-archive
        # https://www.gnu.org/software/autoconf-archive/ax_lua.html
        if '+shared' in spec:
            with working_dir(prefix.lib):
                # e.g., liblua.so.5.1.5
                src_path = 'liblua.{0}.{1}'.format(dso_suffix,
                                                   str(self.version.up_to(3)))

                # For lua version 5.1.X, the symlinks should be:
                # liblua5.1.so
                # liblua51.so
                # liblua-5.1.so
                # liblua-51.so
                version_formats = [str(self.version.up_to(2)),
                                   Version(str(self.version.up_to(2))).joined]
                for version_str in version_formats:
                    for joiner in ['', '-']:
                        dest_path = 'liblua{0}{1}.{2}'.format(joiner,
                                                              version_str,
                                                              dso_suffix)
                        os.symlink(src_path, dest_path)

        with working_dir(os.path.join('luarocks', 'luarocks')):
            configure('--prefix=' + prefix, '--with-lua=' + prefix)
            make('build')
            make('install')

    def append_paths(self, paths, cpaths, path):
        paths.append(os.path.join(path, '?.lua'))
        paths.append(os.path.join(path, '?', 'init.lua'))
        if '+shared' in self.spec:
            cpaths.append(os.path.join(path, '?.so'))

    def _setup_dependent_env_helper(self, env, dependent_spec):
        lua_paths = []
        for d in dependent_spec.traverse(
                deptypes=('build', 'run'), deptype_query='run'):
            if d.package.extends(self.spec):
                lua_paths.append(os.path.join(d.prefix, self.lua_lib_dir))
                lua_paths.append(os.path.join(d.prefix, self.lua_lib64_dir))
                lua_paths.append(os.path.join(d.prefix, self.lua_share_dir))

        lua_patterns = []
        lua_cpatterns = []
        for p in lua_paths:
            if os.path.isdir(p):
                self.append_paths(lua_patterns, lua_cpatterns, p)

        # Always add this package's paths
        for p in (os.path.join(self.spec.prefix, self.lua_lib_dir),
                  os.path.join(self.spec.prefix, self.lua_lib64_dir),
                  os.path.join(self.spec.prefix, self.lua_share_dir)):
            self.append_paths(lua_patterns, lua_cpatterns, p)

        return lua_patterns, lua_cpatterns

    def setup_dependent_build_environment(self, env, dependent_spec):
        lua_patterns, lua_cpatterns = self._setup_dependent_env_helper(
            env, dependent_spec)

        env.set('LUA_PATH', ';'.join(lua_patterns), separator=';')
        if '+shared' in self.spec:
            env.set('LUA_CPATH', ';'.join(lua_cpatterns), separator=';')

    def setup_dependent_run_environment(self, env, dependent_spec):
        # For run time environment set only the path for dependent_spec and
        # prepend it to LUAPATH
        lua_patterns, lua_cpatterns = self._setup_dependent_env_helper(
            env, dependent_spec)

        if dependent_spec.package.extends(self.spec):
            env.prepend_path('LUA_PATH', ';'.join(lua_patterns), separator=';')
            if '+shared' in self.spec:
                env.prepend_path('LUA_CPATH', ';'.join(lua_cpatterns),
                                 separator=';')

    def setup_run_environment(self, env):
        env.prepend_path(
            'LUA_PATH',
            os.path.join(self.spec.prefix, self.lua_share_dir, '?.lua'),
            separator=';')
        env.prepend_path(
            'LUA_PATH', os.path.join(self.spec.prefix, self.lua_share_dir, '?',
                                     'init.lua'),
            separator=';')
        env.prepend_path(
            'LUA_PATH',
            os.path.join(self.spec.prefix, self.lua_lib_dir, '?.lua'),
            separator=';')
        env.prepend_path(
            'LUA_PATH',
            os.path.join(self.spec.prefix, self.lua_lib_dir, '?', 'init.lua'),
            separator=';')
        if '+shared' in self.spec:
            env.prepend_path(
                'LUA_CPATH',
                os.path.join(self.spec.prefix, self.lua_lib_dir, '?.so'),
                separator=';')

    @run_after('install')
    def link_pkg_config(self):
        if "+pcfile" in self.spec:
            symlink(join_path(self.prefix.lib, 'pkgconfig', 'lua5.3.pc'),
                    join_path(self.prefix.lib, 'pkgconfig', 'lua.pc'))

    @property
    def lua_lib_dir(self):
        return os.path.join('lib', 'lua', str(self.version.up_to(2)))

    @property
    def lua_lib64_dir(self):
        return os.path.join('lib64', 'lua', str(self.version.up_to(2)))

    @property
    def lua_share_dir(self):
        return os.path.join('share', 'lua', str(self.version.up_to(2)))

    def setup_dependent_package(self, module, dependent_spec):
        """
        Called before lua modules's install() methods.

        In most cases, extensions will only need to have two lines::

        luarocks('--tree=' + prefix, 'install', rock_spec_path)
        """
        # Lua extension builds can have lua and luarocks executable functions
        module.lua = Executable(join_path(self.spec.prefix.bin, 'lua'))
        module.luarocks = Executable(
            join_path(self.spec.prefix.bin, 'luarocks'))
