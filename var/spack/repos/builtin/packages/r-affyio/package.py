# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffyio(RPackage):
    """Tools for parsing Affymetrix data files.

       Routines for parsing Affymetrix data files based upon file format
       information. Primary focus is on accessing the CEL and CDF file
       formats."""

    homepage = "https://bioconductor.org/packages/affyio"
    git      = "https://git.bioconductor.org/packages/affyio.git"

    version('1.54.0', commit='c0e306e1805a556a1074d1af1acdd18e0a04477f')
    version('1.52.0', commit='9da725ac1098a22a370fa96eb03e51e4f6d5d963')
    version('1.50.0', commit='911ea4f8e4cdf7b649b87ef7ed1a5f5b111ef38a')
    version('1.48.0', commit='01727a4492c3a0d50453fc91892e04bf5f7fcadb')
    version('1.46.0', commit='977597f2772e08273d86579486f452170566c880')

    depends_on('r@2.6.0:', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
