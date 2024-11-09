# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Pixman(AutotoolsPackage):
    """The Pixman package contains a library that provides low-level
    pixel manipulation features such as image compositing and
    trapezoid rasterization."""

    homepage = "https://www.pixman.org"
    url = "https://cairographics.org/releases/pixman-0.32.6.tar.gz"

    license("MIT")

    version("0.42.2", sha256="ea1480efada2fd948bc75366f7c349e1c96d3297d09a3fe62626e38e234a625e")
    version("0.42.0", sha256="07f74c8d95e4a43eb2b08578b37f40b7937e6c5b48597b3a0bb2c13a53f46c13")
    version("0.40.0", sha256="6d200dec3740d9ec4ec8d1180e25779c00bc749f94278c8b9021f5534db223fc")
    version("0.38.4", sha256="da66d6fd6e40aee70f7bd02e4f8f76fc3f006ec879d346bae6a723025cfbdde7")
    version("0.38.0", sha256="a7592bef0156d7c27545487a52245669b00cf7e70054505381cff2136d890ca8")
    version("0.34.0", sha256="21b6b249b51c6800dc9553b65106e1e37d0e25df942c90531d4c3997aa20a88e")
    version("0.32.6", sha256="3dfed13b8060eadabf0a4945c7045b7793cc7e3e910e748a8bb0f0dc3e794904")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("flex", type="build")
    depends_on("bison@3:", type="build")
    depends_on("libpng")

    variant("shared", default=True, description="Build shared library")

    # As discussed here:
    # https://bugs.freedesktop.org/show_bug.cgi?id=104886
    # __builtin_shuffle was removed in clang 5.0.
    # From version 9.1 apple-clang is based on clang 5.0.
    # Patch is obtained from above link.
    patch("clang.patch", when="@0.34%apple-clang@9.1.0:")
    patch("clang.patch", when="@0.34%clang@5.0.0:")

    @run_before("build")
    def patch_config_h_for_intel(self):
        config_h = join_path(self.stage.source_path, "config.h")

        # Intel disguises itself as GNU, but doesn't implement
        # the same builtin functions. This causes in this case
        # a positive detection of GCC vector extensions, which
        # is bound to fail at compile time because Intel has no
        # __builtin_shuffle. See also:
        #
        # https://software.intel.com/en-us/forums/intel-c-compiler/topic/758013
        #
        if "%intel" in self.spec:
            filter_file(
                r"#define HAVE_GCC_VECTOR_EXTENSIONS /\*\*/",
                "/* #undef HAVE_GCC_VECTOR_EXTENSIONS */",
                config_h,
            )

    @property
    def libs(self):
        return find_libraries(
            "libpixman-1", self.prefix, shared=self.spec.satisfies("+shared"), recursive=True
        )

    def configure_args(self):
        args = ["--enable-libpng", "--disable-gtk", "--with-pic"]

        if sys.platform == "darwin":
            args += ["--disable-mmx", "--disable-silent-rules"]

            # From homebrew, see:
            #  https://gitlab.freedesktop.org/pixman/pixman/-/issues/59
            #  https://gitlab.freedesktop.org/pixman/pixman/-/issues/69
            if self.spec.target.family == "aarch64":
                args.append("--disable-arm-a64-neon")

        # The Fujitsu compiler does not support assembler macros.
        if self.spec.satisfies("%fj"):
            args.append("--disable-arm-a64-neon")

        args.extend(self.enable_or_disable("shared"))

        return args
