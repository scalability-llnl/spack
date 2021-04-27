# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRex(RPackage):
    """Friendly Regular Expressions

    A friendly interface for the construction of regular expressions."""

    homepage = "https://cloud.r-project.org/package=rex"
    url      = "https://cloud.r-project.org/src/contrib/rex_1.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rex"

    version('1.2.0', sha256='06b491f1469078862e40543fd74e1d38b2e0fb61fdf01c8083add4b11ac2eb54')
    version('1.1.2', sha256='bd3c74ceaf335336f5dd04314d0a791f6311e421a2158f321f5aab275f539a2a')

    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-magrittr', when='@:1.1.2', type=('build', 'run'))
