# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSys(RPackage):
    """Powerful and Reliable Tools for Running System Commands in R.

    Drop-in replacements for the base system2() function with fine control and
    consistent behavior across platforms. Supports clean interruption, timeout,
    background tasks, and streaming STDIN / STDOUT / STDERR over binary or text
    connections. Arguments on Windows automatically get encoded and quoted to
    work on different locales."""

    cran = "sys"

    license("MIT")

    version("3.4.2", sha256="b7bdce66f0fb681830ea6fb77b5a2c6babb43920abb1eddc733f95c0a63ce5b3")
    version("3.4.1", sha256="324e6d8fde58264e62bc04867b719c5fd16296de1542689801b8cb13621ecf52")
    version("3.4", sha256="17f88fbaf222f1f8fd07919461093dac0e7175ae3c3b3264b88470617afd0487")
    version("3.2", sha256="2819498461fe2ce83d319d1a47844e86bcea6d01d10861818dba289e7099bbcc")

    def flag_handler(self, name, flags):
        if name == "cflags":
            flags.append(self.compiler.c99_flag)
        return (flags, None, None)
