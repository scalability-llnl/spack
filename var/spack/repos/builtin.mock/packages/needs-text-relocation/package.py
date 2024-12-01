# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class NeedsTextRelocation(Package):
    """A dumy package that encodes its prefix."""

    homepage = "https://www.cmake.org"
    url = "https://cmake.org/files/v3.4/cmake-3.4.3.tar.gz"

    version("0.0.0", md5="12345678qwertyuiasdfghjkzxcvbnm0")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        exe = join_path(prefix.bin, "exe")
        with open(exe, "w") as f:
            f.write(prefix)
        set_executable(exe)

        otherexe = join_path(prefix.bin, "otherexe")
        with open(otherexe, "w") as f:
            f.write("Lorem Ipsum")
        set_executable(otherexe)
