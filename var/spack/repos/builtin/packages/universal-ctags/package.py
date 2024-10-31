# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UniversalCtags(AutotoolsPackage):
    """Universal Ctags generates an index (or tag) file of language
    objects found in source files for many popular programming languages.
    This index makes it easy for text editors and other tools to locate
    the indexed items."""

    homepage = "https://ctags.io/"
    url = "https://github.com/universal-ctags/ctags/archive/p5.9.20210912.0.tar.gz"
    git = "https://github.com/universal-ctags/ctags.git"

    license("GPL-2.0-or-later")

    version("master", branch="master")
    version(
        "6.1.20240505.0", sha256="d9329d9d28c8280fcf8626594813958d9f90160ad6c7f10b0341a577d5b53527"
    )
    version(
        "5.9.20210912.0", sha256="5082d4f7e5695be3d697c46e2232d76c6d8adff51d22ba7a4b869362f444ee21"
    )
    version(
        "5.9.20210808.0", sha256="7f5f88d20750dfa2437ca9d163972b8684e3cf16de022a5177f322be92f528cc"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("iconv", type="link")
    depends_on("pkgconfig", type="build")

    def autoreconf(self, spec, prefix):
        which("bash")("autogen.sh")
