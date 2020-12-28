# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# See the Spack documentation for more information on packaging.

from spack.package import *


class RXnomial(RPackage):
    """XNomial: Exact Goodness-of-Fit Test for Multinomial Data with Fixed
       Probabilities"""

    homepage = "https://cloud.r-project.org/package=XNomial"
    url      = "https://cloud.r-project.org/src/contrib/XNomial_1.0.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/XNomial/"

    version('1.0.4', sha256='e6237f79d96f02bb30af1cf055ae9f70541abba34ce045a9d4359b5304189dd7')

    depends_on('r@2.14:', type=('build', 'run'))
