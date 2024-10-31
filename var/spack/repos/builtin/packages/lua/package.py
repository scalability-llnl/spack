# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from llnl.util.symlink import readlink

import spack.build_environment
from spack.package import *
from spack.util.executable import Executable


class LuaImplPackage(MakefilePackage):
    """Specialized class for lua *implementations*

    This exists to ensure that lua, luajit and luajit-openresty all initialize extension
    packages the same way and provide luarocks the same way."""

    extendable = True

    variant(
        "fetcher",
        default="curl",
        values=("curl", "wget"),
        description="Fetcher to use in the LuaRocks package manager",
    )

    lua_version_override = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lua_dir_name = "lua"
        pass

    def __verdir(self):
        return (
            str(self.version.up_to(2))
            if self.lua_version_override is None
            else self.lua_version_override
        )

    @property
    def lua_lib_dir(self):
        return os.path.join("lib", self.lua_dir_name, self.__verdir())

    @property
    def lua_lib64_dir(self):
        return os.path.join("lib64", self.lua_dir_name, self.__verdir())

    @property
    def lua_share_dir(self):
        return os.path.join("share", self.lua_dir_name, self.__verdir())

    # luarocks needs unzip for some packages (e.g. lua-luaposix)
    depends_on("unzip", type=("build", "run"))

    # luarocks needs a fetcher (curl/wget), unfortunately I have not found
    # how to force a choice for curl or wget, but curl seems the default.
    depends_on("curl", when="fetcher=curl", type="run")
    depends_on("wget", when="fetcher=wget", type="run")

    resource(
        name="luarocks",
        url="https://luarocks.github.io/luarocks/releases/luarocks-3.11.1.tar.gz",
        sha256="c3fb3d960dffb2b2fe9de7e3cb004dc4d0b34bb3d342578af84f84325c669102",
        destination="luarocks",
        placement="luarocks",
    )

    def symlink_luajit(self):
        """helper for luajit-like packages that need symlinks"""
        if not self.spec.satisfies("+lualinks"):
            return

        with working_dir(self.prefix.bin):
            if not os.path.exists(self.prefix.bin.lua):
                luajits = find(self.prefix.bin, "luajit*")
                assert len(luajits) >= 1
                luajit = luajits[0]
                if os.path.islink(luajit):
                    luajit = readlink(luajit)
                symlink(luajit, "lua")

        with working_dir(self.prefix.include):
            if not os.path.exists(self.prefix.include.lua):
                luajit_include_subdirs = glob.glob(os.path.join(self.prefix.include, "luajit*"))
                assert len(luajit_include_subdirs) == 1
                symlink(luajit_include_subdirs[0], "lua")

        with working_dir(self.prefix.lib):
            for ext in ("." + spack.build_environment.dso_suffix, ".a"):
                luajit_libnames = glob.glob(
                    os.path.join(self.prefix.lib, "libluajit") + "*" + ext + "*"
                )
                real_lib = next(
                    lib
                    for lib in luajit_libnames
                    if os.path.isfile(lib) and not os.path.islink(lib)
                )
                symlink(real_lib, "liblua" + ext)

    @run_after("install")
    def add_luarocks(self):
        prefix = self.spec.prefix
        with working_dir(os.path.join("luarocks", "luarocks")):
            configure("--prefix=" + prefix, "--with-lua=" + prefix)
            make("build")
            make("install")

    def append_paths(self, paths, cpaths, path):
        paths.append(os.path.join(path, "?.lua"))
        paths.append(os.path.join(path, "?", "init.lua"))
        cpaths.append(os.path.join(path, "?.so"))

    def _setup_dependent_env_helper(self, env, dependent_spec):
        lua_paths = []
        for d in dependent_spec.traverse(deptype=("build", "run")):
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
        for p in (
            os.path.join(self.spec.prefix, self.lua_lib_dir),
            os.path.join(self.spec.prefix, self.lua_lib64_dir),
            os.path.join(self.spec.prefix, self.lua_share_dir),
        ):
            self.append_paths(lua_patterns, lua_cpatterns, p)

        return lua_patterns, lua_cpatterns

    def setup_dependent_build_environment(self, env, dependent_spec):
        lua_patterns, lua_cpatterns = self._setup_dependent_env_helper(env, dependent_spec)

        env.prepend_path("LUA_PATH", ";".join(lua_patterns), separator=";")
        env.prepend_path("LUA_CPATH", ";".join(lua_cpatterns), separator=";")

    def setup_dependent_run_environment(self, env, dependent_spec):
        # For run time environment set only the path for dependent_spec and
        # prepend it to LUAPATH
        lua_patterns, lua_cpatterns = self._setup_dependent_env_helper(env, dependent_spec)

        if dependent_spec.package.extends(self.spec):
            env.prepend_path("LUA_PATH", ";".join(lua_patterns), separator=";")
            env.prepend_path("LUA_CPATH", ";".join(lua_cpatterns), separator=";")

    def setup_run_environment(self, env):
        env.prepend_path(
            "LUA_PATH", os.path.join(self.spec.prefix, self.lua_share_dir, "?.lua"), separator=";"
        )
        env.prepend_path(
            "LUA_PATH",
            os.path.join(self.spec.prefix, self.lua_share_dir, "?", "init.lua"),
            separator=";",
        )
        env.prepend_path(
            "LUA_PATH", os.path.join(self.spec.prefix, self.lua_lib_dir, "?.lua"), separator=";"
        )
        env.prepend_path(
            "LUA_PATH",
            os.path.join(self.spec.prefix, self.lua_lib_dir, "?", "init.lua"),
            separator=";",
        )
        env.prepend_path(
            "LUA_CPATH", os.path.join(self.spec.prefix, self.lua_lib_dir, "?.so"), separator=";"
        )

    @property
    def lua(self):
        return Executable(self.spec.prefix.bin.lua)

    @property
    def luarocks(self):
        return Executable(self.spec.prefix.bin.luarocks)

    def setup_dependent_package(self, module, dependent_spec):
        """
        Called before lua modules's install() methods.

        In most cases, extensions will only need to have two lines::

            luarocks('--tree=' + prefix, 'install', rock_spec_path)
        """
        # Lua extension builds can have lua and luarocks executable functions
        module.lua = Executable(self.spec.prefix.bin.lua)
        module.luarocks = Executable(self.spec.prefix.bin.luarocks)


class Lua(LuaImplPackage):
    """The Lua programming language interpreter and library."""

    homepage = "https://www.lua.org"
    url = "https://www.lua.org/ftp/lua-5.3.4.tar.gz"

    version("5.4.6", sha256="7d5ea1b9cb6aa0b59ca3dde1c6adcb57ef83a1ba8e5432c0ecd06bf439b3ad88")
    version("5.4.4", sha256="164c7849653b80ae67bec4b7473b884bf5cc8d2dca05653475ec2ed27b9ebf61")
    version("5.4.3", sha256="f8612276169e3bfcbcfb8f226195bfc6e466fe13042f1076cbde92b7ec96bbfb")
    version("5.4.2", sha256="11570d97e9d7303c0a59567ed1ac7c648340cd0db10d5fd594c09223ef2f524f")
    version("5.4.1", sha256="4ba786c3705eb9db6567af29c91a01b81f1c0ac3124fdbf6cd94bdd9e53cca7d")
    version("5.4.0", sha256="eac0836eb7219e421a96b7ee3692b93f0629e4cdb0c788432e3d10ce9ed47e28")
    version("5.3.6", sha256="fc5fd69bb8736323f026672b1b7235da613d7177e72558893a0bdcd320466d60")
    version("5.3.5", sha256="0c2eed3f960446e1a3e4b9a1ca2f3ff893b6ce41942cf54d5dd59ab4b3b058ac")
    version("5.3.4", sha256="f681aa518233bc407e23acf0f5887c884f17436f000d453b2491a9f11a52400c")
    version("5.3.2", sha256="c740c7bb23a936944e1cc63b7c3c5351a8976d7867c5252c8854f7b2af9da68f")
    version("5.3.1", sha256="072767aad6cc2e62044a66e8562f51770d941e972dc1e4068ba719cd8bffac17")
    version("5.3.0", sha256="ae4a5eb2d660515eb191bfe3e061f2b8ffe94dce73d32cfd0de090ddcc0ddb01")
    version("5.2.4", sha256="b9e2e4aad6789b3b63a056d442f7b39f0ecfca3ae0f1fc0ae4e9614401b69f4b")
    version("5.2.3", sha256="13c2fb97961381f7d06d5b5cea55b743c163800896fd5c5e2356201d3619002d")
    version("5.2.2", sha256="3fd67de3f5ed133bf312906082fa524545c6b9e1b952e8215ffbd27113f49f00")
    version("5.2.1", sha256="64304da87976133196f9e4c15250b70f444467b6ed80d7cfd7b3b982b5177be5")
    version("5.2.0", sha256="cabe379465aa8e388988073d59b69e76ba0025429d2c1da80821a252cdf6be0d")
    version("5.1.5", sha256="2640fc56a795f29d28ef15e13c34a47e223960b0240e8cb0a82d9b0738695333")
    version("5.1.4", sha256="b038e225eaf2a5b57c9bcc35cd13aa8c6c8288ef493d52970c9545074098af3a")
    version("5.1.3", sha256="6b5df2edaa5e02bf1a2d85e1442b2e329493b30b0c0780f77199d24f087d296d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("pcfile", default=False, description="Add patch for lua.pc generation")
    variant("shared", default=True, description="Builds a shared version of the library")

    provides("lua-lang@5.1", when="@5.1:5.1.99")
    provides("lua-lang@5.2", when="@5.2:5.2.99")
    provides("lua-lang@5.3", when="@5.3:5.3.99")
    provides("lua-lang@5.4", when="@5.4:5.4.99")

    depends_on("ncurses+termlib")
    depends_on("readline")

    patch(
        "http://lua.2524044.n2.nabble.com/attachment/7666421/0/pkg-config.patch",
        sha256="208316c2564bdd5343fa522f3b230d84bd164058957059838df7df56876cb4ae",
        when="+pcfile @:5.3.9999",
    )

    def build(self, spec, prefix):
        if spec.satisfies("platform=darwin"):
            target = "macosx"
        else:
            target = "linux"
        make(
            "MYLDFLAGS="
            + " ".join((spec["readline"].libs.search_flags, spec["ncurses"].libs.search_flags)),
            "MYLIBS=%s" % spec["ncurses"].libs.link_flags,
            "CC={0} -std=gnu99 {1}".format(spack_cc, self.compiler.cc_pic_flag),
            target,
        )

    def install(self, spec, prefix):
        make("INSTALL_TOP=%s" % prefix, "install")

        if spec.satisfies("+shared"):
            static_to_shared_library(
                join_path(prefix.lib, "liblua.a"),
                arguments=["-lm", "-ldl"],
                version=self.version,
                compat_version=self.version.up_to(2),
            )

        # compatibility with ax_lua.m4 from autoconf-archive
        # https://www.gnu.org/software/autoconf-archive/ax_lua.html
        if spec.satisfies("+shared"):
            with working_dir(prefix.lib):
                # e.g., liblua.so.5.1.5
                src_path = "liblua.{0}.{1}".format(dso_suffix, str(self.version.up_to(3)))

                # For lua version 5.1.X, the symlinks should be:
                # liblua5.1.so
                # liblua51.so
                # liblua-5.1.so
                # liblua-51.so
                version_formats = [
                    str(self.version.up_to(2)),
                    Version(str(self.version.up_to(2))).joined,
                ]
                for version_str in version_formats:
                    for joiner in ["", "-"]:
                        dest_path = "liblua{0}{1}.{2}".format(joiner, version_str, dso_suffix)
                        os.symlink(src_path, dest_path)

    @run_after("install")
    def link_pkg_config(self):
        if self.spec.satisfies("+pcfile"):
            versioned_pc_file_name = "lua{0}.pc".format(self.version.up_to(2))
            symlink(
                join_path(self.prefix.lib, "pkgconfig", versioned_pc_file_name),
                join_path(self.prefix.lib, "pkgconfig", "lua.pc"),
            )
