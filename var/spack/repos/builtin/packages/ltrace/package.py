# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ltrace(AutotoolsPackage):
    """Ltrace intercepts and records dynamic library calls which are called
    by an executed process and the signals received by that process. It
    can also intercept and print the system calls executed by the program."""

    homepage = "https://www.ltrace.org"
    url = "https://www.ltrace.org/ltrace_0.7.3.orig.tar.bz2"

    license("GPL-2.0-or-later")

    version("0.7.3", sha256="0e6f8c077471b544c06def7192d983861ad2f8688dd5504beae62f0c5f5b9503")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    conflicts("platform=darwin", msg="ltrace runs only on Linux.")

    depends_on("elf", type="link")

    def configure_args(self):
        # Disable -Werror since some functions used by ltrace
        # have been deprecated in recent version of glibc
        return ["--disable-werror"]
