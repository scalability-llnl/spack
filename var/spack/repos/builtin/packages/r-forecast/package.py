# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RForecast(RPackage):
    """Methods and tools for displaying and analysing univariate time
    series forecasts including exponential smoothing via state space
    models and automatic ARIMA modelling."""

    homepage = "https://cloud.r-project.org/package=forecast"
    url      = "https://cloud.r-project.org/src/contrib/forecast_8.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/forecast"

    version('8.6', sha256='4279e4f700e26310bae39419ab4a9b5918a850148667a5e577a4807d53eb4d02')
    version('8.2', '3ef095258984364c100b771b3c90d15e')

    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-ggplot2@2.2.1:', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-fracdiff', type=('build', 'run'))
    depends_on('r-tseries', type=('build', 'run'))
    depends_on('r-lmtest', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-timedate', type=('build', 'run'))
    depends_on('r-rcpparmadillo@0.2.35:', type=('build', 'run'))
    depends_on('r-urca', when='@8.6:', type=('build', 'run'))
