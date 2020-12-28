# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDeoptimr(RPackage):
    """An implementation of a bespoke jDE variant of the Differential
       Evolution stochastic algorithm for global optimization of
       nonlinear programming problems."""

    homepage = "https://cloud.r-project.org/package=DEoptimR"
    url      = "https://cloud.r-project.org/src/contrib/DEoptimR_1.0-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/DEoptimR"

    version('1.0-8', sha256='846911c1b2561a9fae73a8c60a21a5680963ebb0050af3c1f1147ae9a121e5ef')
