# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRook(RPackage):
    """This package contains the Rook specification and convenience software
    for building and running Rook applications. To get started, be sure and
    read the 'Rook' help file first."""

    homepage = "https://cloud.r-project.org/package=Rook"
    url      = "https://cloud.r-project.org/src/contrib/Rook_1.1-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Rook"

    version('1.1-1', sha256='00f4ecfa4c5c57018acbb749080c07154549a6ecaa8d4130dd9de79427504903')

    depends_on('r@2.13.0:', type=('build', 'run'))
    depends_on('r-brew', type=('build', 'run'))
