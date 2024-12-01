# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Glibc(AutotoolsPackage, GNUMirrorPackage):
    """The GNU C Library provides many of the low-level components used
    directly by programs written in the C or C++ languages.
    """

    homepage = "https://www.gnu.org/software/libc/"
    gnu_mirror_path = "libc/glibc-2.33.tar.gz"
    git = "https://sourceware.org/git/glibc.git"

    tags = ["runtime"]

    provides("libc")

    version("2.39", sha256="97f84f3b7588cd54093a6f6389b0c1a81e70d99708d74963a2e3eab7c7dc942d")
