# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nextdenovo(MakefilePackage):
    """NextDenovo is a string graph-based de novo assembler for long reads."""

    homepage = "https://nextdenovo.readthedocs.io/en/latest/index.html"
    url = "https://github.com/Nextomics/NextDenovo/archive/refs/tags/2.5.2.tar.gz"

    license("GPL-3.0-only")

    version("2.5.2", sha256="f1d07c9c362d850fd737c41e5b5be9d137b1ef3f1aec369dc73c637790611190")

    depends_on("c", type="build")  # generated

    depends_on("python", type="run")
    depends_on("py-paralleltask", type="run")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter(r"^TOP_DIR.*", "TOP_DIR={0}".format(self.build_directory))
        runfile = FileFilter("nextDenovo")
        runfile.filter(r"^SCRIPT_PATH.*", "SCRIPT_PATH = '{0}'".format(prefix))

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install("nextDenovo", prefix.bin)
        install_tree("lib", prefix.lib)
