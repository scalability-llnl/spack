# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RSys(RPackage):
    """Powerful and Reliable Tools for Running System Commands in R

    Drop-in replacements for the base system2() function with fine control
    and consistent behavior across platforms. Supports clean interruption,
    timeout, background tasks, and streaming STDIN / STDOUT / STDERR over
    binary or text connections. Arguments on Windows automatically get encoded
    and quoted to work on different locales."""

    homepage = "https://github.com/jeroen/sys#readme"
    url      = "https://cloud.r-project.org/src/contrib/sys_3.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/sys"

    version('3.4', sha256='17f88fbaf222f1f8fd07919461093dac0e7175ae3c3b3264b88470617afd0487')
    version('3.2', sha256='2819498461fe2ce83d319d1a47844e86bcea6d01d10861818dba289e7099bbcc')

    def flag_handler(self, name, flags):
        if name == 'cflags':
            flags.append(self.compiler.c99_flag)
        return (flags, None, None)
