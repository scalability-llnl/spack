# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class Cln(AutotoolsPackage):
    """CLN is a library for efficient computations with all kinds of numbers
    in arbitrary precision. It features number classes for unlimited length
    integers, rationals, arbitrary precision floating point numbers and much
    more."""

    homepage = "https://www.ginac.de/CLN/"
    url = "https://www.ginac.de/CLN/cln-1.3.7.tar.bz2"
    git = "git://www.ginac.de/cln.git"
    maintainers("prudhomm")

    license("GPL-2.0-or-later")

    version("master", branch="master")
    version("1.3.7", commit="bc36e1e941c9296f37198c3125ac7f2b2ca4f48b")
    version("1.3.6", commit="d4ba1cc869be2c647c4ab48ac571b1fc9c2021a9")
    version("1.3.5", commit="b221c033c082b462455502b7e63702a9c466aede")
    version("1.3.4", commit="9b86a7fc69feb1b288469982001af565f73057eb")
    version("1.3.3", commit="1c9bd61ff0b89b0bf8030e44cb398e8f75112222")
    version("1.3.2", commit="00817f7b60a961b860f6d305ac82dd51b70d6ba6")
    version("1.3.1", commit="196fee3778494b69063f2a1b018e70de351b336f")
    version("1.3.0", commit="8e19c1a9d9ea4116112490d6f43904258b928649")
    version("1.2.2", commit="cd3ea9b9889856c6b54266fdb13b54dd3c53931a")
    version("1.2.1", commit="567378ab4cbfd443c3d82d810599860c769251fe")
    version("1.2.0", commit="679a0a8927f011fb32411f8a31070c77a9901094")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("gmp", default=True, description="Enable GMP multiprecision library")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("gmp@4.1:", when="+gmp")
    depends_on("texinfo", type="build")

    # Dependencies required to define macro AC_LIB_LINKFLAGS_FROM_LIBS
    depends_on("gettext", type="build")

    def autoreconf(self, spec, prefix):
        autoreconf_args = ["-i"]

        aclocal_pkg_list = ["gettext"]
        aclocal_path = os.path.join("share", "aclocal")

        for pkg in aclocal_pkg_list:
            autoreconf_args += ["-I", os.path.join(spec[pkg].prefix, aclocal_path)]

        autoreconf = which("autoreconf")
        autoreconf(*autoreconf_args)

    @run_before("autoreconf")
    def force_config_rpath(self):
        source_directory = self.stage.source_path
        build_aux_directory = os.path.join(source_directory, "build-aux")

        mkdir = which("mkdir")
        mkdir(build_aux_directory)

        touch = which("touch")
        touch(os.path.join(build_aux_directory, "config.rpath"))

    def configure_args(self):
        spec = self.spec

        configure_args = []

        if spec.satisfies("+gmp"):
            configure_args.append("--with-gmp={0}".format(spec["gmp"].prefix))
        else:
            configure_args.append("--without-gmp")

        return configure_args
