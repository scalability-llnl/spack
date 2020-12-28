# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRrblup(RPackage):
    """rrBLUP: Ridge Regression and Other Kernels for Genomic Selection"""

    homepage = "http://potatobreeding.cals.wisc.edu/software"
    url      = "https://cloud.r-project.org/src/contrib/rrBLUP_4.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rrBLUP"

    version('4.6', sha256='28b475a1466fcdc1780caace75cf34155338fda496cebd5799315598a4bc84af')

    depends_on('r@2.14:', type=('build', 'run'))
