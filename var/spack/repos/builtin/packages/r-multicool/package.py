# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMulticool(RPackage):
    """Permutations of multisets in cool-lex order."""

    homepage = "https://cloud.r-project.org/package=multicool"
    url      = "https://cloud.r-project.org/src/contrib/Archive/multicool/multicool_0.1-9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/multicool/Archive/multicool"

    version('0.1-9', sha256='bdf92571cef1b649952d155395a92b8683099ee13114f73a9d41fc5d7d49d329')

    depends_on('r-rcpp@0.11.2:', type=('build', 'run'))
