# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DialignTx(MakefilePackage):
    """DIALIGN-TX: greedy and progressive approaches for segment-based
    multiple sequence alignment"""

    homepage = "https://dialign-tx.gobics.de/"
    url = "https://dialign-tx.gobics.de/DIALIGN-TX_1.0.2.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.0.2", sha256="fb3940a48a12875332752a298f619f0da62593189cd257d28932463c7cebcb8f")

    build_directory = "source"

    conflicts("%gcc@6:")

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter("Makefile")
            makefile.filter(" -march=i686 ", " ")
            makefile.filter("CC=gcc", "CC=%s" % spack_cc)
            if spec.target.family == "aarch64":
                makefile.filter("-mfpmath=sse -msse  -mmmx", " ")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install("dialign-tx", prefix.bin)
            # t-coffee recognizes as dialign-t
            install("dialign-tx", join_path(prefix.bin, "dialign-t"))
