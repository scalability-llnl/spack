# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RChron(RPackage):
    """Chronological objects which can handle dates and times."""

    homepage = "https://cloud.r-project.org/package=chron"
    url      = "https://cloud.r-project.org/src/contrib/chron_2.3-47.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/chron"

    version('2.3-53', sha256='521814b46ba958eae28e29d8766aebd285da5e6fa16c5806603df3ae39f77309')
    version('2.3-52', sha256='c47fcf4abb635babe6337604c876d4853d8a24639a98b71523746c56ce75b4a0')
    version('2.3-47', sha256='9a8c771021165de517e54c3369c622aaac1bf3e220a2fbf595aba285e60445f6')

    depends_on('r@2.12.0:', type=('build', 'run'))
