# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.builtin.lua import LuaImplPackage


class LuaLuajit(LuaImplPackage):
    """Flast flexible JITed lua"""

    homepage = "https://www.luajit.org"
    url = "https://luajit.org/download/LuaJIT-2.0.5.tar.gz"

    license("MIT")

    version(
        "2.1.0-beta3", sha256="1ad2e34b111c802f9d0cdf019e986909123237a28c746b21295b63c9e785d9c3"
    )
    version(
        "2.0.5",
        sha256="874b1f8297c697821f561f9b73b57ffd419ed8f4278c82e05b48806d30c1e979",
        preferred=True,
    )
    version("2.0.4", sha256="620fa4eb12375021bef6e4f237cbd2dd5d49e56beb414bee052c746beef1807d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    conflicts("@:2.0.5", when="target=aarch64:")

    variant(
        "lualinks",
        default=True,
        description="add symlinks to make lua-luajit a drop-in lua replacement",
    )

    provides("luajit", "lua-lang@5.1", when="+lualinks")
    lua_version_override = "5.1"
    conflicts("platform=darwin", msg="luajit not supported on MacOS, see lua-luajit-openresty")

    @run_after("install")
    def install_links(self):
        self.symlink_luajit()

    @property
    def headers(self):
        hdrs = find_headers("luajit", self.prefix.include, recursive=True)
        hdrs.directories = os.path.dirname(hdrs[0])
        return hdrs or None

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("PREFIX= .*", "PREFIX = {0}".format(prefix))
        src_makefile = FileFilter(join_path("src", "Makefile"))
        src_makefile.filter("^DEFAULT_CC = .*", "DEFAULT_CC = {0}".format(spack_cc))
        src_makefile.filter(
            "^DYNAMIC_CC = .*", "DYNAMIC_CC = $(CC) {0}".format(self.compiler.cc_pic_flag)
        )

        # Linking with the C++ compiler is a dirty hack to deal with the fact
        # that unwinding symbols are not included by libc, this is necessary
        # on some platforms for the final link stage to work
        src_makefile.filter("^TARGET_LD = .*", "TARGET_LD = {0}".format(spack_cxx))
