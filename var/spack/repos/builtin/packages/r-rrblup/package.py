# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRrblup(RPackage):
    """Ridge Regression and Other Kernels for Genomic Selection

    Software for genomic prediction with the RR-BLUP mixed model (Endelman
    2011, <doi:10.3835/plantgenome2011.08.0024>). One application is to
    estimate marker effects by ridge regression; alternatively, BLUPs can be
    calculated based on an additive relationship matrix or a Gaussian
    kernel."""

    homepage = "http://potatobreeding.cals.wisc.edu/software"
    url      = "https://cloud.r-project.org/src/contrib/rrBLUP_4.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rrBLUP"

    version('4.6.1', sha256='e9230e74cc430a83ac5567071cb1c7f00b35c368f7d79bcc1cfde7225446c4db')
    version('4.6', sha256='28b475a1466fcdc1780caace75cf34155338fda496cebd5799315598a4bc84af')

    depends_on('r@2.14:', type=('build', 'run'))
