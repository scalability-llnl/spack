# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from llnl.util.filesystem import find

import spack.builder
import spack.package_base
import spack.util.executable
from spack.directives import build_system, depends_on, extends
from spack.multimethod import when


class LuaPackage(spack.package_base.PackageBase):
    """Specialized class for lua packages"""

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "LuaPackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "lua"

    list_depth = 1  # LuaRocks requires at least one level of spidering to find versions

    build_system("lua")

    with when("build_system=lua"):
        depends_on("lua-lang")
        with when("^[virtuals=lua-lang] lua"):
            extends("lua")
        with when("^[virtuals=lua-lang] lua-luajit"):
            extends("lua-luajit+lualinks")
        with when("^[virtuals=lua-lang] lua-luajit-openresty"):
            extends("lua-luajit-openresty+lualinks")

    @property
    def lua(self):
        return spack.util.executable.Executable(self.spec["lua-lang"].prefix.bin.lua)

    @property
    def luarocks(self):
        lr = spack.util.executable.Executable(self.spec["lua-lang"].prefix.bin.luarocks)
        return lr


@spack.builder.builder("lua")
class LuaBuilder(spack.builder.Builder):
    phases = ("unpack", "generate_luarocks_config", "preprocess", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("luarocks_args",)

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = ()

    def unpack(self, pkg, spec, prefix):
        if os.path.splitext(pkg.stage.archive_file)[1] == ".rock":
            directory = pkg.luarocks("unpack", pkg.stage.archive_file, output=str)
            dirlines = directory.split("\n")
            # TODO: figure out how to scope this better
            os.chdir(dirlines[2])

    @staticmethod
    def _generate_tree_line(name, prefix):
        return """{{ name = "{name}", root = "{prefix}" }};""".format(name=name, prefix=prefix)

    def generate_luarocks_config(self, pkg, spec, prefix):
        spec = self.pkg.spec
        table_entries = []
        for d in spec.traverse(deptype=("build", "run")):
            if d.package.extends(self.pkg.extendee_spec):
                table_entries.append(self._generate_tree_line(d.name, d.prefix))

        path = self._luarocks_config_path()
        with open(path, "w") as config:
            config.write(
                """
                deps_mode="all"
                rocks_trees={{
                {}
                }}
                """.format(
                    "\n".join(table_entries)
                )
            )
        return path

    def preprocess(self, pkg, spec, prefix):
        """Override this to preprocess source before building with luarocks"""
        pass

    def luarocks_args(self):
        return []

    def install(self, pkg, spec, prefix):
        rock = "."
        specs = find(".", "*.rockspec", recursive=False)
        if specs:
            rock = specs[0]
        rocks_args = self.luarocks_args()
        rocks_args.append(rock)
        self.pkg.luarocks("--tree=" + prefix, "make", *rocks_args)

    def _luarocks_config_path(self):
        return os.path.join(self.pkg.stage.source_path, "spack_luarocks.lua")

    def setup_build_environment(self, env):
        env.set("LUAROCKS_CONFIG", self._luarocks_config_path())
