# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIsdparser(RPackage):
    """isdparser: Parse 'NOAA' Integrated Surface Data Files"""

    homepage = "https://github.com/ropensci/isdparser"
    url      = "https://cloud.r-project.org/src/contrib/isdparser_0.3.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/isdparser"

    version('0.3.0', sha256='6c9e1d7f3661802838010d659d7c77b964423dcc9a6623402df1fe3be627b7b9')

    depends_on('r-data-table@1.10.0:', type=('build', 'run'))
    depends_on('r-tibble@1.2:', type=('build', 'run'))
