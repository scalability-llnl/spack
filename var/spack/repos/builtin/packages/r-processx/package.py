# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProcessx(RPackage):
    """Tools to run system processes in the background"""

    homepage = "https://github.com/r-lib/processx"
    url      = "https://cloud.r-project.org/src/contrib/processx_3.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/processx"

    version('3.4.1', sha256='f1abddb48fa78f2b176552e2ec5d808d4d87d79ce72e9b3d25c9a7d715bbd1bc')
    version('3.3.1', sha256='6123dbdf9f3bb6e5e8678980fb4587dcefb56d2190adf2ef494d7cd199720bae')
    version('3.2.0', sha256='c4ba602fcbdc032ae9d94701b3e6b83a2dab1b53d0b4f9937b07a84eae22fddf')
    version('3.1.0',   sha256='11ac120ab4e4aa0e99c9b2eda87d07bc683bab735f1761e95e5ddacd311b5972')
    version('3.0.3',   sha256='53781dba3c538605a02e28b3b577e7de79e2064bfc502025f7ec0e5945e302bf')
    version('2.0.0.1', sha256='8f61b2952d0f2d13c74465bfba174ce11eee559475c2f7b9be6bcb9e2e1d827b')
    version('2.0.0',   sha256='8325b56a60a276909228756281523cda9256bc754c5f3ca03b41c5c17cc398ad')

    depends_on('r-assertthat', when='@:3.2.9', type=('build', 'run'))
    depends_on('r-crayon', when='@:3.2.9', type=('build', 'run'))
    depends_on('r-ps@1.2.0:', when='@3.2.0:', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-debugme', when='@:3.0.9', type=('build', 'run'))
