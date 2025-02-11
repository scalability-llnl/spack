# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Flook(MakefilePackage):
    """Flook is a fortran-Lua-hook library."""

    homepage = "http://electronicstructurelibrary.github.io/flook/doxygen/index.html"
    git = "https://github.com/ElectronicStructureLibrary/flook"

    version("0.8.1", tag="v0.8.1", commit="56d22fb9d8e461d13d0d19c1208c31c70ae8d895")

    def edit(self, spec, prefix):
        # Use the Spack compiler wrappers
        os.rename(".setup.make", "setup.make")
        setup_make = FileFilter("setup.make")
        setup_make.filter("CC = .*", "CC = {0}".format(spack_cc))
        setup_make.filter("FC = .*", "FC = {0}".format(spack_f77))

        lua_makefile = FileFilter("aotus/external/lua-5.3.5/src/Makefile")
        lua_makefile.filter("CC= .*", "CC = {0}".format(spack_cc))

    def build(self, spec, prefix):
        make("liball")

    def install(self, spec, prefix):
        make("PREFIX={0}".format(prefix), "install")
        aotus_modfiles = glob.iglob("aotus/obj/*.mod")
        for mod in aotus_modfiles:
            install(mod, prefix.include)
