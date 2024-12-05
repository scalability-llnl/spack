# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDomc(RPackage):
    """Foreach Parallel Adaptor for 'parallel'.

    Provides a parallel backend for the %dopar% function using the multicore
    functionality of the parallel package."""

    cran = "doMC"

    version("1.3.8", sha256="b2186f851448251ae6af5d14b9e3e7f9221f90887e5f8de6a68c91caf16619a3")
    version("1.3.7", sha256="defab27adc298a6746896d83251f8355d62c01012d51ef96d491875a2e74b54d")
    version("1.3.6", sha256="2977fc9e2dc54d85d45b4a36cd286dff72834fbc73f38b6ee45a6eb8557fc9b2")
    version("1.3.4", sha256="76a1092fca59b441e6f89eb7e2fb3a12de807f736a217949c80339f20c958778")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r-foreach@1.2.0:", type=("build", "run"))
    depends_on("r-iterators@1.0.0:", type=("build", "run"))
