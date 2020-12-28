# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPrettyunits(RPackage):
    """Pretty, human readable formatting of quantities. Time intervals:
       1337000 -> 15d 11h 23m 20s. Vague time intervals: 2674000 -> about
       a month ago. Bytes: 1337 -> 1.34 kB."""

    homepage = "https://cloud.r-project.org/package=prettyunits"
    url      = "https://cloud.r-project.org/src/contrib/prettyunits_1.0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/prettyunits"

    version('1.0.2', sha256='35a4980586c20650538ae1e4fed4d80fdde3f212b98546fc3c7d9469a1207f5c')

    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-assertthat', type=('build', 'run'))
