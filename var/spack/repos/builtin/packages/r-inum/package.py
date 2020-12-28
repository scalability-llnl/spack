# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RInum(RPackage):
    """Enum-type representation of vectors and representation of intervals,
    including a method of coercing variables in data frames."""

    homepage = "https://cloud.r-project.org/package=inum"
    url      = "https://cloud.r-project.org/src/contrib/inum_1.0-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/inum"

    version('1.0-1', sha256='3c2f94c13c03607e05817e4859595592068b55e810fed94e29bc181ad248a099')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-libcoin@1.0-0:', type=('build', 'run'))
