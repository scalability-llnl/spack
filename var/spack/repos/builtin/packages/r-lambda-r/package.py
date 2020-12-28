# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLambdaR(RPackage):
    """A language extension to efficiently write functional programs in R.
       Syntax extensions include multi-part function definitions, pattern
       matching, guard statements, built-in (optional) type safety."""

    homepage = "https://cloud.r-project.org/package=lambda.r"
    url      = "https://cloud.r-project.org/src/contrib/lambda.r_1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lambda.r"

    version('1.2.3', sha256='0cd8e37ba1a0960888016a85d492da51a57df54bd65ff920b08c79a3bfbe8631')
    version('1.2', sha256='7dc4188ce1d4a6b026a1b128719ff60234ae1e3ffa583941bbcd8473ad18146f')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-formatr', type=('build', 'run'))
