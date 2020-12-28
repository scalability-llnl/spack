# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Hercules(MakefilePackage):
    """Hercules is an amazingly fast and highly customizable Git
    repository analysis engine written in Go."""

    homepage = "https://github.com/src-d/hercules"
    url      = "https://github.com/src-d/hercules/archive/v10.7.2.tar.gz"

    version('10.7.2', sha256='4654dcfb1eee5af1610fd05677c6734c2ca1161535fcc14d3933d6debda4bc34')

    depends_on('protobuf', type='build')
    depends_on('go@1.11:', type='build')
    depends_on('py-labours', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('hercules', prefix.bin)
