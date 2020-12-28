# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spades(CMakePackage):
    """SPAdes - St. Petersburg genome assembler - is intended for both
       standard isolates and single-cell MDA bacteria assemblies."""

    homepage = "http://cab.spbu.ru/software/spades/"
    url      = "http://cab.spbu.ru/files/release3.10.1/SPAdes-3.10.1.tar.gz"

    version('3.14.1', sha256='d629b78f7e74c82534ac20f5b3c2eb367f245e6840a67b9ef6a76f6fac5323ca')
    version('3.13.0', sha256='c63442248c4c712603979fa70503c2bff82354f005acda2abc42dd5598427040')
    version('3.12.0', sha256='15b48a3bcbbe6a8ad58fd04ba5d3f1015990fbfd9bdf4913042803b171853ac7')
    version('3.11.1', sha256='3ab85d86bf7d595bd8adf11c971f5d258bbbd2574b7c1703b16d6639a725b474')
    version('3.10.1', sha256='d49dd9eb947767a14a9896072a1bce107fb8bf39ed64133a9e2f24fb1f240d96')

    depends_on('python', type=('build', 'run'))
    depends_on('zlib')
    depends_on('bzip2')

    # SPAdes will explicitly not compile with gcc < 5.3.0
    conflicts('%gcc@:5.2.9')

    conflicts('%gcc@7.1.0:', when='@:3.10.1')

    root_cmakelists_dir = "src"
