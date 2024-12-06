# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRCache(RPackage):
    """Fast and Light-Weight Caching (Memoization) of Objects and Results to
    Speed Up Computations.

    Memoization can be used to speed up repetitive and computational expensive
    function calls. The first time a function that implements memoization is
    called the results are stored in a cache memory. The next time the function
    is called with the same set of parameters, the results are momentarily
    retrieved from the cache avoiding repeating the calculations. With this
    package, any R object can be cached in a key-value storage where the key
    can be an arbitrary set of R objects. The cache memory is persistent (on
    the file system)."""

    cran = "R.cache"

    version("0.16.0", sha256="7853409161571a790e0383f64f99e4eae43201a0ed7146d2baf157741a509291")
    version("0.15.0", sha256="adb4d3b08f7917e10fe6188c7b90a3318701a974c58eaa09943b929382bdf126")
    version("0.14.0", sha256="18af4e372440b9f28b4b71346c8ed9de220232f9903730ccee2bfb3c612c16d9")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r-r-methodss3@1.7.1:", type=("build", "run"))
    depends_on("r-r-methodss3@1.8.1:", type=("build", "run"), when="@0.15.0:")
    depends_on("r-r-oo@1.23.0:", type=("build", "run"))
    depends_on("r-r-oo@1.24.0:", type=("build", "run"), when="@0.15.0:")
    depends_on("r-r-utils@2.8.0:", type=("build", "run"))
    depends_on("r-r-utils@2.10.1:", type=("build", "run"), when="@0.15.0:")
    depends_on("r-digest@0.6.13:", type=("build", "run"))
