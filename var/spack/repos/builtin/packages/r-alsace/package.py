# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAlsace(RPackage):
    """ALS for the Automatic Chemical Exploration of mixtures.

    Alternating Least Squares (or Multivariate Curve Resolution) for
    analytical chemical data, in particular hyphenated data where the first
    direction is a retention time axis, and the second a spectral axis.
    Package builds on the basic als function from the ALS package and adds
    functionality for high-throughput analysis, including definition of time
    windows, clustering of profiles, retention time correction, etcetera."""

    bioc = "alsace"

    version("1.30.0", commit="d0e09b283da2b4869d5d6e6801399676246bc5bc")
    version("1.26.0", commit="40a76404acb1466723a78a55d87c67eec3e6f306")
    version("1.20.0", commit="47f1cf8daafc864e5e3418009f349ce85d6b0389")
    version("1.18.0", commit="c9fc43c7b441de43b14ef1be69926c4c4a566191")
    version("1.16.0", commit="5a51a19aeccbba0123222201cb7a228559f29653")
    version("1.14.0", commit="aebb13b00eb850f9569391c4c92183b55b70ae89")
    version("1.12.0", commit="1364c65bbff05786d05c02799fd44fd57748fae3")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-als", type=("build", "run"))
    depends_on("r-ptw@1.0.6:", type=("build", "run"))
