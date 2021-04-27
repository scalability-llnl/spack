# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAmelia(RPackage):
    """Amelia: A Program for Missing Data

    Amelia II "multiply imputes" missing data in a single
    cross-section (such as a survey), from a time series (like
    variables collected for each year in a country), or from a
    time-series-cross-sectional data set (such as collected by
    years for each of several countries)."""

    homepage = "http://gking.harvard.edu/amelia"
    url      = "https://cloud.r-project.org/src/contrib/Amelia_1.7.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Amelia"

    version('1.7.6',  sha256='63c08d374aaf78af46c34dc78da719b3085e58d9fabdc76c6460d5193a621bea')

    depends_on('r@3.0.2:',        type=('build', 'run'))
    depends_on('r-rcpp@0.11:',    type=('build', 'run'))
    depends_on('r-foreign',       type=('build', 'run'))
    depends_on('r-rcpparmadillo', type=('build', 'run'))
