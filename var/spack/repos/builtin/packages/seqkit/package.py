# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Seqkit(Package):
    """A cross-platform and ultrafast toolkit for FASTA/Q file manipulation
    in Golang."""

    homepage = "http://bioinf.shenwei.me/seqkit"
    url      = "https://github.com/shenwei356/seqkit/releases/download/v0.10.1/seqkit_linux_amd64.tar.gz"

    version('0.10.1', sha256='82f1c86dc4bd196403a56c2bf3ec063e5674a71777e68d940c4cc3d8411d2e9d')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('seqkit', prefix.bin)
