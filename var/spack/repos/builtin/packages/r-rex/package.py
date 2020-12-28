# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRex(RPackage):
    """A friendly interface for the construction of regular expressions."""

    homepage = "https://cloud.r-project.org/package=rex"
    url      = "https://cloud.r-project.org/src/contrib/rex_1.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rex"

    version('1.1.2', sha256='bd3c74ceaf335336f5dd04314d0a791f6311e421a2158f321f5aab275f539a2a')

    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
