# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bedtools2(Package):
    """Collectively, the bedtools utilities are a swiss-army knife of
       tools for a wide-range of genomics analysis tasks. The most
       widely-used tools enable genome arithmetic: that is, set theory
       on the genome."""

    homepage = "https://github.com/arq5x/bedtools2"
    url      = "https://github.com/arq5x/bedtools2/archive/v2.26.0.tar.gz"

    version('2.29.2', sha256='bc2f36b5d4fc9890c69f607d54da873032628462e88c545dd633d2c787a544a5')
    version('2.27.1', sha256='edcac089d84e63a51f85c3c189469daa7d42180272130b046856faad3cf79112')
    version('2.27.0', sha256='e91390b567e577d337c15ca301e264b0355441f5ab90fa4f971622e3043e0ca0')
    version('2.26.0', sha256='15db784f60a11b104ccbc9f440282e5780e0522b8d55d359a8318a6b61897977')
    version('2.25.0', sha256='159122afb9978015f7ec85d7b17739b01415a5738086b20a48147eeefcf08cfb')
    version('2.23.0', sha256='9dacaa561d11ce9835d1d51e5aeb092bcbe117b7119663ec9a671abac6a36056')

    depends_on('zlib')
    depends_on('bzip2', when='@2.29:')
    depends_on('xz', when='@2.29:')
    depends_on('python', type='build')

    def install(self, spec, prefix):
        make("prefix=%s" % prefix, "install")
