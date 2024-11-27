# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RParallelmap(RPackage):
    """Unified Interface to Parallelization Back-Ends.

    Unified parallelization framework for multiple back-end, designed for
    internal package and interactive usage. The main operation is a parallel
    "map" over lists. Supports local, multicore, mpi and BatchJobs mode.
    Allows "tagging" of the parallel operation with a level name that can be
    later selected by the user to switch on parallel execution for exactly this
    operation."""

    cran = "parallelMap"

    version("1.5.1", sha256="c108a634a335ed47b0018f532a52b032487e239c5061f939ba32355dfefde7e1")
    version("1.5.0", sha256="4afa727f4786279718cc799e45e91859a46f5cbc1ee652b0f47ae3b9f9d45e4e")
    version("1.4", sha256="fb6f15e325f729f1c5218768b17c20909ee857069c6cc5d8df50e1dafe26ed5b")
    version("1.3", sha256="a52d93572c1b85281e41d8e3c2db97dda5fce96c222e04171b4489ec5000cd08")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-bbmisc@1.8:", type=("build", "run"))
    depends_on("r-checkmate@1.8.0:", type=("build", "run"))
