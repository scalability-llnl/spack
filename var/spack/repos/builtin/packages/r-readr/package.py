# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RReadr(RPackage):
    """The goal of 'readr' is to provide a fast and friendly way to read
       rectangular data (like 'csv', 'tsv', and 'fwf'). It is designed to
       flexibly parse many types of data found in the wild, while still cleanly
       failing when data unexpectedly changes."""

    homepage = "https://cloud.r-project.org/package=readr"
    url      = "https://cloud.r-project.org/src/contrib/readr_1.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/readr"

    version('1.3.1', sha256='33f94de39bb7f2a342fbb2bd4e5afcfec08798eac39672ee18042ac0b349e4f3')
    version('1.1.1', sha256='1a29b99009a06f2cee18d08bc6201fd4985b6d45c76cefca65084dcc1a2f7cb3')

    depends_on('r@3.0.2:', when='@:1.2.1', type=('build', 'run'))
    depends_on('r@3.1:', when='@1.3.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.0.5:', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-hms@0.4.1:', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'run'))
    depends_on('r-clipr', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-crayon', when='@1.3.1:', type=('build', 'run'))
    depends_on('gmake', type='build')
