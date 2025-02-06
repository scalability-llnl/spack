# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RForecast(RPackage):
    """Forecasting Functions for Time Series and Linear Models.

    Methods and tools for displaying and analysing univariate time series
    forecasts including exponential smoothing via state space models and
    automatic ARIMA modelling."""

    cran = "forecast"

    license("GPL-3.0-only")

    version("8.23.0", sha256="ffc3d41138f498fb286f0ebfeb72d15f9f7a8e953abf3c351ebf95fc188a1880")
    version("8.21", sha256="fdd131795a9d3fb399d76a9aa66a0c276637caaa9ec0c75fbe386189d005c6c2")
    version("8.18", sha256="5920baa8d9d81988000d0e2edcea61c05126b5cb923cb5921a6fcd7bc312d8dd")
    version("8.16", sha256="9f01eb895a883a7e1e23725b167b46edc1b0b152fd4120278aaa5f7b2621767f")
    version("8.15", sha256="c73aabed083095b457ed875c240716686fbd41d1cbafa116b7b890a54b919174")
    version("8.13", sha256="490e3a2beb71c238dd26e7afa0b33394b9906dd0dc54712d4808894d5aa1386f")
    version("8.8", sha256="d077074d77d3ea00e9215c828b3689a8c841a16af1e6859bb2dfdede081c2c1d")
    version("8.6", sha256="4279e4f700e26310bae39419ab4a9b5918a850148667a5e577a4807d53eb4d02")
    version("8.2", sha256="eb3fab64ed139d068e7d026cd3880f1b623f4153a832fb71845488fa75e8b812")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@8.18:")
    depends_on("r-colorspace", type=("build", "run"))
    depends_on("r-fracdiff", type=("build", "run"))
    depends_on("r-generics@0.1.2:", type=("build", "run"), when="@8.18:")
    depends_on("r-ggplot2@2.2.1:", type=("build", "run"))
    depends_on("r-lmtest", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-nnet", type=("build", "run"))
    depends_on("r-rcpp@0.11.0:", type=("build", "run"))
    depends_on("r-timedate", type=("build", "run"))
    depends_on("r-tseries", type=("build", "run"))
    depends_on("r-urca", type=("build", "run"), when="@8.6:")
    depends_on("r-withr", type=("build", "run"), when="@8.23.0:")
    depends_on("r-zoo", type=("build", "run"))
    depends_on("r-rcpparmadillo@0.2.35:", type=("build", "run"))
