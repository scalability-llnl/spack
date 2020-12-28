# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHms(RPackage):
    """Implements an S3 class for storing and formatting time-of-day values,
       based on the 'difftime' class."""

    homepage = "https://cloud.r-project.org/package=hms"
    url      = "https://cloud.r-project.org/src/contrib/hms_0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/hms"

    version('0.5.0', sha256='a87872665c3bf3901f597d78c152e7805f7129e4dbe27397051de4cf1a76561b')
    version('0.3', sha256='9368259cbc1094ce0e4cf61544875ec30088ef690d6667e6b0b564218ab3ff88')

    depends_on('r-pkgconfig', when='@0.5.0:', type=('build', 'run'))
    depends_on('r-rlang', when='@0.5.0:', type=('build', 'run'))
    depends_on('r-vctrs@0.2.0:', when='@0.5.0:', type=('build', 'run'))
