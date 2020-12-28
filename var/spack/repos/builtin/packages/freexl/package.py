# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Freexl(AutotoolsPackage):
    """FreeXL is an open source library to extract valid data from within
       an Excel (.xls) spreadsheet."""

    homepage = "http://www.gaia-gis.it"
    url      = "http://www.gaia-gis.it/gaia-sins/freexl-1.0.5.tar.gz"

    version('1.0.5', sha256='3dc9b150d218b0e280a3d6a41d93c1e45f4d7155829d75f1e5bf3e0b0de6750d')
