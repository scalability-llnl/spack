# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libiconv(AutotoolsPackage, GNUMirrorPackage):
    """GNU libiconv provides an implementation of the iconv() function
    and the iconv program for character set conversion."""

    homepage = "https://www.gnu.org/software/libiconv/"
    gnu_mirror_path = "libiconv/libiconv-1.16.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.17", sha256="8f74213b56238c85a50a5329f77e06198771e70dd9a739779f4c02f65d971313")
    version("1.16", sha256="e6a1b1b589654277ee790cce3734f07876ac4ccfaecbee8afa0b649cf529cc04")
    version("1.15", sha256="ccf536620a45458d26ba83887a983b96827001e92a13847b45e4925cc8913178")
    version("1.14", sha256="72b24ded17d687193c3366d0ebe7cde1e6b18f0df8c55438ac95be39e8a30613")

    depends_on("c", type="build")  # generated

    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )

    # We cannot set up a warning for gets(), since gets() is not part
    # of C11 any more and thus might not exist.
    patch("gets.patch", when="@1.14")
    provides("iconv")

    conflicts("@1.14", when="%gcc@5:")

    def configure_args(self):
        args = ["--enable-extra-encodings"]

        args += self.enable_or_disable("libs")
        args.append("--with-pic")

        # Starting version 1.17, libiconv uses the version of gnulib that implements a
        # configure-time check for C compiler flags that enables/disables certain warning
        # (see https://git.savannah.gnu.org/gitweb/?p=gnulib.git;h=0c8a563f6). Unfortunately, the
        # check does not work for compilers that inject extra symbols into the translation unit
        # during the preprocessing step. For example, NVHPC injects the definition of the
        # __va_list_tag structure, which appears verbatim on the compilation command line as
        # additional compiler flags. The easiest way to circumvent the issue is to make the
        # configure script believe that the compiler does not support a flag that allows warnings:
        if self.spec.satisfies("@1.17:%nvhpc"):
            args.append("gl_cv_cc_wallow=none")

        # A hack to patch config.guess in the libcharset sub directory
        copy("./build-aux/config.guess", "libcharset/build-aux/config.guess")
        return args

    @property
    def libs(self):
        shared = self.spec.satisfies("libs=shared")
        return find_libraries(["libiconv"], root=self.prefix, recursive=True, shared=shared)
