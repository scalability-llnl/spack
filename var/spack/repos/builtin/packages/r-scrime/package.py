# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScrime(RPackage):
    """scrime: Analysis of High-Dimensional Categorical Data Such as SNP
       Data"""

    homepage = "https://cloud.r-project.org/package=scrime"
    url      = "https://cloud.r-project.org/src/contrib/scrime_1.3.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/scrime"

    version('1.3.5', sha256='5d97d3e57d8eb30709340fe572746029fd139456d7a955421c4e3aa75d825578')
