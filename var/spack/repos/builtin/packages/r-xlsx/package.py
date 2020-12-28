# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXlsx(RPackage):
    """Provide R functions to read/write/format Excel 2007 and Excel
    97/2000/XP/2003 file formats."""

    homepage = "http://code.google.com/p/rexcel/"
    url      = "https://cloud.r-project.org/src/contrib/xlsx_0.6.1.tar.gz"
    listurl  = "https://cloud.r-project.org/src/contrib/Archive/xlsx"

    version('0.6.1', sha256='a580bd16b5477c1c185bf681c12c1ffff4088089f97b6a37997913d93ec5a8b4')

    depends_on('r-rjava', type=('build', 'run'))
    depends_on('r-xlsxjars', type=('build', 'run'))
    depends_on('java@1.6:')
