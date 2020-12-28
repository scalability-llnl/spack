# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMultitaper(RPackage):
    """multitaper: Spectral Analysis Tools using the Multitaper Method"""

    homepage = "https://github.com/krahim/multitaper/"
    url      = "https://cloud.r-project.org/src/contrib/multitaper_1.0-14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/multitaper/"

    version('1.0-14', sha256='c84c122541dc2874131446e23b212259b3b00590d701efee49e6740fd74a8d13')

    depends_on('r@3.0:', type=('build', 'run'))
