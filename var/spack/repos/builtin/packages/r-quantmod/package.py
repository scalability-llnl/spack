# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQuantmod(RPackage):
    """Specify, build, trade, and analyse quantitative financial trading
    strategies."""

    homepage = "http://www.quantmod.com/"
    url      = "https://cloud.r-project.org/src/contrib/quantmod_0.4-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/quantmod"

    version('0.4-15', sha256='7ef2e798d4d8e4d2af0a5b2b9fecebec30568087afbd24bfd923cdeb8b53df53')
    version('0.4-14', sha256='d95b1acf73328d675bbad18a93fa3c40faf58959e0401458ad21cf6b9f9254b3')
    version('0.4-10', sha256='030040aa567adaba1ea4a1f05eb45712dbdaabbabca72733e7fb2984051f688b')
    version('0.4-5', sha256='c7889eb55a21296e7bda1242c46e734a0a8bd6dcbf5726aafae5313354eec893')

    depends_on('r@3.2.0:', when='@0.4-11:', type=('build', 'run'))
    depends_on('r-xts@0.9-0:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-ttr@0.2:', type=('build', 'run'))
    depends_on('r-curl', type=('build', 'run'))
