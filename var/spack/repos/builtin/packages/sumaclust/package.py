# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sumaclust(MakefilePackage):
    """Sumaclust aims to cluster sequences in a way that is fast and exact at
    the same time."""

    homepage = "https://git.metabarcoding.org/obitools/sumaclust"

    license("CECILL-2.0")

    version(
        "1.0.20",
        sha256="b697495f9a2b93fe069ecdb3bc6bba75b07ec3ef9f01ed66c4dd69587a40cfc1",
        url="https://git.metabarcoding.org/obitools/sumaclust/uploads/69f757c42f2cd45212c587e87c75a00f/sumaclust_v1.0.20.tar.gz",
    )

    def build(self, spec, prefix):
        make("CC={0}".format(spack_cc))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("sumaclust", prefix.bin)
