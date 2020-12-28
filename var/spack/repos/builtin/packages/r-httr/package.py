# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHttr(RPackage):
    """Useful tools for working with HTTP organised by HTTP verbs (GET(),
    POST(), etc). Configuration functions make it easy to control additional
    request components (authenticate(), add_headers() and so on)."""

    homepage = "https://github.com/hadley/httr"
    url      = "https://cloud.r-project.org/src/contrib/httr_1.2.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/httr"

    version('1.4.1', sha256='675c7e07bbe82c48284ee1ab929bb14a6e653abae2860d854dc41a3c028de156')
    version('1.4.0', sha256='d633f1425da514f65f3b8c034ae0a8b6911995009840c6bb9657ceedb99ddb48')
    version('1.3.1', sha256='22134d7426b2eba37f0cc34b99285499b8bac9fe75a7bc3222fbad179bf8f258')
    version('1.2.1', sha256='e7b90b90ee52c826e152efcfadf98e078fa75b65a6baaeb8fd25eeed2195730e')
    version('1.1.0', sha256='d7c0cdc11b2ded3132544580f52ebe5dad2a426cde1a5029f2cc693b2f195823')

    depends_on('r@3.0.0:', when='@:1.3.1', type=('build', 'run'))
    depends_on('r@3.1:', when='@1.4.0', type=('build', 'run'))
    depends_on('r@3.2:', when='@1.4.1:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-mime', type=('build', 'run'))
    depends_on('r-curl@3.0.0:', type=('build', 'run'))
    depends_on('r-openssl@0.8:', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
