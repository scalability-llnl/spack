# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBfast(RPackage):
    """Breaks for Additive Season and Trend.

    Decomposition of time series into trend, seasonal, and remainder components
    with methods for detecting and characterizing abrupt changes within the
    trend and seasonal components. 'BFAST' can be used to analyze different
    types of satellite image time series and can be applied to other
    disciplines dealing with seasonal or non-seasonal time series, such as
    hydrology, climatology, and econometrics. The algorithm can be extended to
    label detected changes with information on the parameters of the fitted
    piecewise linear models. 'BFAST' monitoring functionality is described in
    Verbesselt et al. (2010) <doi:10.1016/j.rse.2009.08.014>. 'BFAST monitor'
    provides functionality to detect disturbance in near real-time based on
    'BFAST'- type models, and is described in Verbesselt et al. (2012)
    <doi:10.1016/j.rse.2012.02.022>. 'BFAST Lite' approach is a flexible
    approach that handles missing data without interpolation, and will be
    described in an upcoming paper. Furthermore, different models can now be
    used to fit the time series data and detect structural changes (breaks)."""

    cran = "bfast"

    license("GPL-2.0-or-later")

    version("1.6.1", sha256="aaf479af1924691cbec8c67c68005c00d97cead51b2b44863c18acd4cea453ee")
    version("1.5.7", sha256="01585fe8944d05ebdb13795214077bc1365f0c0372e2a1f7edb914356dace558")

    depends_on("cxx", type="build")  # generated

    depends_on("r@2.15.0:", type=("build", "run"))
    depends_on("r@3.0.0:", type=("build", "run"), when="@1.6.1:")
    depends_on("r-strucchangercpp", type=("build", "run"), when="@1.6.1:")
    depends_on("r-zoo", type=("build", "run"))
    depends_on("r-forecast", type=("build", "run"))
    depends_on("r-rcpp@0.12.7:", type=("build", "run"), when="@1.6.1:")
    depends_on("r-rdpack@0.7:", type=("build", "run"), when="@1.6.1:")

    depends_on("r-strucchange", type=("build", "run"), when="@:1.5.7")
    depends_on("r-sp", type=("build", "run"), when="@:1.5.7")
    depends_on("r-raster", type=("build", "run"), when="@:1.5.7")
