# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RForeign(RPackage):
    """Functions for reading and writing data stored by some versions of Epi
    Info, Minitab, S, SAS, SPSS, Stata, Systat and Weka and for reading and
    writing some dBase files."""

    homepage = "https://cloud.r-project.org/package=foreign"
    url      = "https://cloud.r-project.org/src/contrib/foreign_0.8-66.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/foreign"

    version('0.8-72', sha256='439c17c9cd387e180b1bb640efff3ed1696b1016d0f7b3b3b884e89884488c88')
    version('0.8-70.2', sha256='ae82fad68159860b8ca75b49538406ef3d2522818e649d7ccc209c18085ef179')
    version('0.8-66', sha256='d7401e5fcab9ce6e697d3520dbb8475e229c30341c0004c4fa489c82aa4447a4')

    depends_on('r@3.0.0:', type=('build', 'run'))
