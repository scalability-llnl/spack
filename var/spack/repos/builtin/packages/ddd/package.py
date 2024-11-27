# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Ddd(AutotoolsPackage, GNUMirrorPackage):
    """A graphical front-end for command-line debuggers such as GDB, DBX,
    WDB, Ladebug, JDB, XDB, the Perl debugger, the bash debugger bashdb,
    the GNU Make debugger remake, or the Python debugger pydb."""

    homepage = "https://www.gnu.org/software/ddd"
    gnu_mirror_path = "ddd/ddd-3.3.12.tar.gz"

    license("LGPL-3.0-only")

    version("3.3.12", sha256="3ad6cd67d7f4b1d6b2d38537261564a0d26aaed077bf25c51efc1474d0e8b65c")

    variant("shared", default=True, description="Build shared libraries")
    variant("static", default=False, description="Build static libraries")

    depends_on("gdb@4.16:")
    depends_on("lesstif@0.89:")
    depends_on("libelf")
    depends_on("readline")
    depends_on("termcap")

    # Patch to fix hangs due to injection of bogus GDB init settings:
    #     https://savannah.gnu.org/bugs/index.php?58191
    patch(
        "https://savannah.gnu.org/bugs/download.php?file_id=48852",
        sha256="8faf986f1dbe529c377f8683deaa8dc2b3b08fe7c297214c9e03860d5c4a1aab",
    )

    # Needed for OSX 10.9 DP6 build failure:
    #     https://savannah.gnu.org/patch/?8178
    patch(
        "https://savannah.gnu.org/patch/download.php?file_id=29114",
        sha256="aaacae79ce27446ead3483123abef0f8222ebc13fd61627bfadad96016248af6",
        working_dir="ddd",
    )

    # https://savannah.gnu.org/bugs/?41997
    patch(
        "https://savannah.gnu.org/patch/download.php?file_id=31132",
        sha256="f3683f23c4b4ff89ba701660031d4b5ef27594076f6ef68814903ff3141f6714",
    )

    # Patch to fix compilation with Xcode 9
    #     https://savannah.gnu.org/bugs/?52175
    patch(
        "https://raw.githubusercontent.com/macports/macports-ports/a71fa9f4/devel/ddd/files/patch-unknown-type-name-a_class.diff",
        sha256="c187a024825144f186f0cf9cd175f3e972bb84590e62079793d0182cb15ca183",
        working_dir="ddd",
    )

    def configure_args(self):
        spec = self.spec

        args = [
            "--disable-debug",
            "--disable-dependency-tracking",
            "--enable-builtin-app-defaults",
            "--enable-builtin-manual",
            "--enable-shared" if "+shared" in spec else "--disable-shared",
            "--enable-static" if "+static" in spec else "--disable-static",
        ]

        return args

    # From MacPorts: make will build the executable "ddd" and the X
    # resource file "Ddd" in the same directory. As HFS+ is case-
    # insensitive by default this will loosely FAIL.  Mitigate this by
    # building/installing 'dddexe' on Darwin and fixing up post install.
    def build(self, spec, prefix):
        make("EXEEXT={0}".format("exe" if spec.satisfies("platform=darwin") else ""))

    # DDD won't install in parallel
    def install(self, spec, prefix):
        make(
            "install",
            "EXEEXT={0}".format("exe" if spec.satisfies("platform=darwin") else ""),
            parallel=False,
        )

    @run_after("install")
    def _rename_exe_on_darwin(self):
        if self.spec.satisfies("platform=darwin"):
            with working_dir(self.prefix.bin):
                os.rename("dddexe", "ddd")
