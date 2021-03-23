# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSystemfonts(RPackage):
    """System Native Font Finding

    Provides system native access to the font catalogue. As font handling
    varies between systems it is difficult to correctly locate installed fonts
    across different operating systems. The 'systemfonts' package provides
    bindings to the native libraries on Windows, macOS and Linux for finding
    font files that can then be used further by e.g. graphic devices. The main
    use is intended to be from compiled code but 'systemfonts' also provides
    access from R."""

    homepage = "https://github.com/r-lib/systemfonts"
    cran     = "systemfonts"

    version('1.0.1', sha256='401db4d9e78e3a5e00b7a0b4fbad7fbb1c584734469b65fe5b7ebe1851c7a797')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-cpp11@0.2.1:', type=('build', 'run'))
    depends_on('fontconfig')
    depends_on('freetype')
