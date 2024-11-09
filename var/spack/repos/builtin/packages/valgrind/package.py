# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import sys

from spack.package import *


class Valgrind(AutotoolsPackage, SourcewarePackage):
    """An instrumentation framework for building dynamic analysis.

    There are Valgrind tools that can automatically detect many memory
    management and threading bugs, and profile your programs in
    detail. You can also use Valgrind to build new tools.

    Valgrind is Open Source / Free Software, and is freely available
    under the GNU General Public License, version 2.
    """

    homepage = "https://valgrind.org/"
    sourceware_mirror_path = "valgrind/valgrind-3.13.0.tar.bz2"
    git = "git://sourceware.org/git/valgrind.git"

    license("GPL-2.0-or-later")

    version("develop", branch="master")
    version("3.23.0", sha256="c5c34a3380457b9b75606df890102e7df2c702b9420c2ebef9540f8b5d56264d")
    version("3.22.0", sha256="c811db5add2c5f729944caf47c4e7a65dcaabb9461e472b578765dd7bf6d2d4c")
    version("3.21.0", sha256="10ce1618bb3e33fad16eb79552b0a3e1211762448a0d7fce11c8a6243b9ac971")
    version("3.20.0", sha256="8536c031dbe078d342f121fa881a9ecd205cb5a78e639005ad570011bdb9f3c6")
    version("3.19.0", sha256="dd5e34486f1a483ff7be7300cc16b4d6b24690987877c3278d797534d6738f02")
    version("3.18.1", sha256="00859aa13a772eddf7822225f4b46ee0d39afbe071d32778da4d99984081f7f5")
    version("3.18.0", sha256="8da880f76592fe8284db98e68f6dc9095485bc2ecc88bc05b7df1f278ae7f657")
    version("3.17.0", sha256="ad3aec668e813e40f238995f60796d9590eee64a16dff88421430630e69285a2")
    version("3.16.1", sha256="c91f3a2f7b02db0f3bc99479861656154d241d2fdb265614ba918cc6720a33ca")
    version("3.15.0", sha256="417c7a9da8f60dd05698b3a7bc6002e4ef996f14c13f0ff96679a16873e78ab1")
    version("3.14.0", sha256="037c11bfefd477cc6e9ebe8f193bb237fe397f7ce791b4a4ce3fa1c6a520baa5")
    version("3.13.0", sha256="d76680ef03f00cd5e970bbdcd4e57fb1f6df7d2e2c071635ef2be74790190c3b")
    version("3.12.0", sha256="67ca4395b2527247780f36148b084f5743a68ab0c850cb43e4a5b4b012cf76a1")
    version("3.11.0", sha256="6c396271a8c1ddd5a6fb9abe714ea1e8a86fce85b30ab26b4266aeb4c2413b42")
    version("3.10.1", sha256="fa253dc26ddb661b6269df58144eff607ea3f76a9bcfe574b0c7726e1dfcb997")
    version("3.10.0", sha256="03047f82dfc6985a4c7d9d2700e17bc05f5e1a0ca6ad902e5d6c81aeb720edc9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Activates MPI support for valgrind")
    variant("boost", default=True, description="Activates boost support for valgrind")
    variant("only64bit", default=True, description="Sets --enable-only64bit option for valgrind")
    variant("ubsan", default=False, description="Activates ubsan support for valgrind")
    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )

    conflicts(
        "+ubsan",
        when="%apple-clang",
        msg="""
Cannot build libubsan with clang on macOS.
Otherwise with (Apple's) clang there is a linker error:
clang: error: unknown argument: '-static-libubsan'
""",
    )
    depends_on("mpi", when="+mpi")
    depends_on("boost+exception+chrono+system+atomic+thread", when="+boost")

    depends_on("autoconf", type="build", when="@develop")
    depends_on("automake", type="build", when="@develop")
    depends_on("libtool", type="build", when="@develop")

    # Apply the patch suggested here:
    # http://valgrind.10908.n7.nabble.com/Unable-to-compile-on-Mac-OS-X-10-11-td57237.html
    patch("valgrind_3_12_0_osx.patch", when="@3.12.0 platform=darwin")

    # Valgrind does not seem to support macOS. As of 3.20.0, the newest version of macOS that is
    # supported by the official repository is 10.13 (macOS High Sierra, released in 2017).
    # There is a fork available with macOS support: https://github.com/LouisBrunner/valgrind-macos
    # However, this fork does not yet support 11+ or M1.
    for os in ["mojave", "catalina", "bigsur", "monterey", "ventura"]:
        conflicts("os=" + os)
    for target in ["m1", "m2"]:
        conflicts("target=" + target)

    def configure_args(self):
        spec = self.spec
        options = self.enable_or_disable("libs")
        if spec.satisfies("+ubsan"):
            options.append("--enable-ubsan")
        if spec.satisfies("+only64bit"):
            options.append("--enable-only64bit")
        if spec.satisfies("~mpi"):
            options.append("--without-mpicc")
        if sys.platform == "darwin":
            options.append("--build=amd64-darwin")
        return options

    # Valgrind the potential for overlong perl shebangs
    def patch(self):
        for link_tool_in in glob.glob("coregrind/link_tool_exe_*.in"):
            filter_file("^#! @PERL@", "#! /usr/bin/env perl", link_tool_in)
