# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTximportdata(RPackage):
    """This packages provides the output of running various transcript abundance
    quantifiers on a set of 6 RNA-seq samples from the GEUVADIS project"""

    homepage = "http://bioconductor.org/packages/release/data/experiment/html/tximportData.html"
    url      = "http://bioconductor.org/packages/release/data/experiment/src/contrib/tximportData_1.18.0.tar.gz"

    version('1.18.0', sha256='4edf9fdcf5b0086fc958d5ac0249668c7cf7e2fa941cd8d413620634d0cb5971')
