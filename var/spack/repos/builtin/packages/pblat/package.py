# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pblat(MakefilePackage):
    """Parallelized blat with multi-threads support"""

    homepage = "http://icebert.github.io/pblat/"
    url = "https://github.com/icebert/pblat/archive/refs/tags/2.5.1.tar.gz"

    # `pblat` shares the license for Jim Kent's `blat`. For-profit users must visit:
    license_url = "https://kentinformatics.com/"

    version("2.5.1", sha256="e85a4d752b8e159502d529f0f9e47579851a6b466b6c2f1f4d49f598642bc615")

    depends_on("c", type="build")  # generated

    depends_on("openssl")
    depends_on("zlib-api")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("MACHTYPE=x86_64", "MACHTYPE?=x86_64")
        makefile.filter("CC=gcc", "")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("pblat", prefix.bin)
