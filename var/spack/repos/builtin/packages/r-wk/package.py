# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RWk(RPackage):
    """Lightweight Well-Known Geometry Parsing

    Provides a minimal R and C++ API for parsing well-known binary and
    well-known text representation of geometries to and from R-native formats.
    Well-known binary is compact and fast to parse; well-known text is
    human-readable and is useful for writing tests. These formats are only
    useful in R if the information they contain can be accessed in R, for which
    high-performance functions are provided here."""

    homepage = "https://paleolimbot.github.io/wk/"
    cran     = "wk"

    version('0.4.1', sha256='daa7351af0bd657740972016906c686f335b8fa922ba10250e5000ddc2bb8950')

    depends_on('r-cpp11', type=('build', 'run'))
