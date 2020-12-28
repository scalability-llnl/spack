# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Miranda(AutotoolsPackage):
    """miRanda is an algorithm for finding genomic targets for microRNAs."""

    homepage = "http://www.microrna.org/microrna/getDownloads.do"
    url      = "http://cbio.mskcc.org/microrna_data/miRanda-aug2010.tar.gz"

    version('3.3a', sha256='a671da562cf4636ef5085b27349df2df2f335774663fd423deb08f31212ec778',
            url='http://cbio.mskcc.org/microrna_data/miRanda-aug2010.tar.gz')
