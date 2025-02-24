# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMrpresso(RPackage):
    """Performs the Mendelian Randomization Pleiotropy RESidual Sum and Outlier
    (MR-PRESSO) test.

    MR-PRESSO (Mendelian Randomization Pleiotropy RESidual Sum and Outlier) is
    a framework that allows for the evaluation of pleiotropy in
    multi-instrument Mendelian Randomization utilizing genome-wide summary
    association statistics."""

    homepage = "https://github.com/rondolab/MR-PRESSO"
    git = "https://github.com/rondolab/MR-PRESSO"

    version("1.0", commit="cece763b47e59763a7916974de43c7cb93843e41")
