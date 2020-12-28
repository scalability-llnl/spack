# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFilehash(RPackage):
    """Implements a simple key-value style database where character string keys
    are associated with data values that are stored on the disk. A simple
    interface is provided for inserting, retrieving, and deleting data from the
    database. Utilities are provided that allow 'filehash' databases to be
    treated much like environments and lists are already used in R. These
    utilities are provided to encourage interactive and exploratory analysis on
    large datasets. Three different file formats for representing the database
    are currently available and new formats can easily be incorporated by third
    parties for use in the 'filehash' framework."""

    homepage = "https://cloud.r-project.org/package=filehash"
    url      = "https://cloud.r-project.org/src/contrib/filehash_2.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/filehash"

    version('2.4-2', sha256='b6d056f75d45e315943a4618f5f62802612cd8931ba3f9f474b595140a3cfb93')
    version('2.4-1', sha256='d0e087d338d89372c251c18fc93b53fb24b1750ea154833216ff16aff3b1eaf4')
    version('2.3', sha256='63b098df9a2cf4aac862cd7bf86ae516e00852a8ad0f3090f9721b6b173e6edb')

    depends_on('r@3.0.0:', type=('build', 'run'))
