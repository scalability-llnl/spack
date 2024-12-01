# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Symlinks(MakefilePackage):
    """Scan or change symbolic links."""

    homepage = "https://ibiblio.org/pub/Linux/utils/file"
    url = "https://ibiblio.org/pub/Linux/utils/file/symlinks-1.4.tar.gz"

    version("1.4", sha256="b0bb689dd0a2c46d9a7dd111b053707aba7b9cf29c4f0bad32984b14bdbe0399")

    depends_on("c", type="build")  # generated

    def edit(self, spec, prefix):
        filter_file("/usr/local", prefix, "Makefile", string=True)
        filter_file("-o root -g root", "", "Makefile")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.man.man8)
        make("install")
