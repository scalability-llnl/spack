# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCountrycode(RPackage):
    """Countrycode standardizes country names, converts them into
    ~40 different coding schemes, and assigns region descriptors."""

    homepage = "https://vincentarelbundock.github.io/countrycode/"
    url      = "https://cloud.r-project.org/src/contrib/countrycode_1.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/countrycode"

    version('1.2.0', sha256='32c65702dcc33d512ff99f14c12f4e0c48fe7ed7c8aa2f0a64194576d129dd40')

    depends_on('r@2.10:', type=('build', 'run'))
