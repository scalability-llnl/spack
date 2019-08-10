# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLambdaR(RPackage):
    """A language extension to efficiently write functional programs in R.
       Syntax extensions include multi-part function definitions, pattern
       matching, guard statements, built-in (optional) type safety."""

    homepage = "https://cran.rstudio.com/web/packages/lambda.r/index.html"
    url      = "https://cran.rstudio.com/src/contrib/lambda.r_1.2.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/lambda.r"

    version('1.2.3', sha256='0cd8e37ba1a0960888016a85d492da51a57df54bd65ff920b08c79a3bfbe8631')
    version('1.2', 'bda49898b85ad5902880a31f43b432e2')

    depends_on('r-formatr', type=('build', 'run'))
