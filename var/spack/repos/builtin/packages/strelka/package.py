# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Strelka(CMakePackage):
    """Somatic and germline small variant caller for mapped sequencing
       data."""

    homepage = "https://github.com/Illumina/strelka"
    url      = "https://github.com/Illumina/strelka/releases/download/v2.8.2/strelka-2.8.2.release_src.tar.bz2"

    version('2.9.10', sha256='45e78efec6e5272697f1d0a95851c7ae0d623dc8f93846e11fe37f15da9f1e30')
    version('2.9.9', sha256='547b42ab983ba38a6459d47e8546daa6d571f370933542f02f3f3bd9abd13c16')
    version('2.9.8', sha256='dc12b894e1267a63f7049bc01402b284db1681c82fb2cac313324a6530cbc4ad')
    version('2.9.7', sha256='9b0db7cc32662488ea53931e1afccff3e7967cd3b492cc93e66a8115a1f4d016')
    version('2.9.6', sha256='db6fe97add75309954bb46f9c53e1c722d8a8d66adc976ff7e2e9788b7ff97fa')
    version('2.9.5', sha256='b3d70129508226280f4de9c328f3cd751e4cedba4383b0264a16ac37f73b1412')
    version('2.9.4', sha256='d06088bb2b033cfcda7263fe8fcf915cba10c77df963f116f64a57cd2682803f')
    version('2.9.3', sha256='9f2cd17b5326f09c499fb01d32d1bb61dec9a97c70199f685824e89bfcad2dee')
    version('2.9.2', sha256='47642c3138e126efaab485a40a9a954abfed34f8c88b107a46dbd64e3f1778a5')
    version('2.9.1', sha256='963e1935389d8777bcdfe77f6126a34a0f8ea5cc27a280e41ba67e9df88cf990')
    version('2.9.0', sha256='25b4dbd270f541bc6a172d12448c209586e9f00e86f56cfce98d1d5612bb4fb8')
    version('2.8.4', sha256='523fb89e7ba7717a61548fcd45b0ccd5c850a8f2b034ab1cf34ec74efb7260c2')
    version('2.8.3', sha256='4f6f8f433a3e1d7a59243bd75bc73dcfb309c1dacc79fe56fafd0ad96e856415')
    version('2.8.2', sha256='27415f7c14f92e0a6b80416283a0707daed121b8a3854196872981d132f1496b')

    depends_on('python@2.4:2.7')
    depends_on('zlib')
    depends_on('bzip2')
    depends_on('cmake@2.8.5:', type='build')
    depends_on('boost@1.56.0:')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
