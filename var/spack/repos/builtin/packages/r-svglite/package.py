# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSvglite(RPackage):
    """An 'SVG' Graphics Device

    A graphics device for R that produces 'Scalable Vector Graphics'. 'svglite'
    is a fork of the older 'RSvgDevice' package."""

    homepage = "https://svglite.r-lib.org/"
    cran     = "svglite"

    version('2.0.0', sha256='76e625fe172a5b7ce99a67b6d631b037b3f7f0021cfe15f2e15e8851b89defa5')

    depends_on('r+X', type=('build', 'run'))
    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-systemfonts@1.0.0:', type=('build', 'run'))
    depends_on('r-cpp11', type=('build', 'run'))
    depends_on('libpng')
