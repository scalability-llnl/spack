# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Weechat(CMakePackage):
    """WeeChat is a fast, light and extensible chat client, with a
    text-based user interface."""

    homepage = "https://weechat.org"
    url = "https://weechat.org/files/src/weechat-2.9.tar.gz"

    license("GPL-3.0-or-later")

    version("2.9", sha256="3a78063b76c42ba306eacf8f74cb8c9a260f8a61d1915d0b5d76f11d2be69a53")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("perl", default=False, description="Include perl support")
    variant("lua", default=False, description="Include lua support")
    variant("ruby", default=False, description="Include ruby support")
    variant("tcl", default=False, description="Include Tcl support")
    variant("guile", default=False, description="Include guile support")
    variant("php", default=False, description="Include php support")

    depends_on("cmake@3:", type="build")
    depends_on("python@3.5:")
    depends_on("gnutls@3.0.21:")
    depends_on("ncurses")
    depends_on("aspell")
    depends_on("libgcrypt")
    depends_on("curl")
    depends_on("zlib-api")
    depends_on("ruby@1.9.1:", when="+ruby")
    depends_on("tcl@8.5:", when="+tcl")
    depends_on("perl", when="+perl")
    depends_on("lua", when="+lua")
    depends_on("guile@2.0:", when="+guile")
    depends_on("php@7.0:", when="+php")

    def cmake_args(self):
        spec = self.spec
        cmake_args = []
        if "~ruby" in spec:
            cmake_args.append("-DENABLE_RUBY=OFF")
        if "~tcl" in spec:
            cmake_args.append("-DENABLE_TCL=OFF")
        if "~perl" in spec:
            cmake_args.append("-DENABLE_PERL=OFF")
        if "~lua" in spec:
            cmake_args.append("-DENABLE_LUA=OFF")
        if "~guile" in spec:
            cmake_args.append("-DENABLE_GUILE=OFF")
        if "~php" in spec:
            cmake_args.append("-DENABLE_PHP=OFF")
        return cmake_args
