# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vsearch(AutotoolsPackage):
    """VSEARCH is a versatile open-source tool for metagenomics."""

    homepage = "https://github.com/torognes/vsearch"
    url      = "https://github.com/torognes/vsearch/archive/v2.4.3.tar.gz"

    version('2.14.1', sha256='388529a39eb0618a09047bf91e0a8ae8c9fd851a05f8d975e299331748f97741')
    version('2.13.3', sha256='e5f34ece28b76403d3ba4a673eca41178fe399c35a1023dbc87d0c0da5efaa52')
    version('2.4.3', sha256='f7ffc2aec5d76bdaf1ffe7fb733102138214cec3e3846eb225455dcc3c088141')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
