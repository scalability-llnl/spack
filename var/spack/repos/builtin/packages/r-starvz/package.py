# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStarvz(RPackage):
    """Performance analysis workflow that combines the power of the R
    language (and the tidyverse realm) and many auxiliary tools to provide
    a consistent, flexible, extensible, fast, and versatile framework for
    the performance analysis of task-based applications that run on top of
    the StarPU runtime (with its MPI (Message Passing Interface) layer for
    multi-node support). Its goal is to provide a fruitful prototypical
    environment to conduct performance analysis hypothesis-checking for
    task-based applications that run on heterogeneous (multi-GPU,
    multi-core) multi-node HPC (High-performance computing) platforms."""

    cran = "starvz"
    git = "https://github.com/schnorr/starvz.git"

    maintainers("viniciusvgp")

    version("0.7.1", sha256="523b35dd3e7679c96087e7e94050c749c55e70ea23a2434f70d701b80b304248")
    version("0.7.0", sha256="9916d5f22052313208b1bdaea2b5e1dc1f4dc804750e9d49d710cc15f3bdd598")
    version("0.6.0", sha256="734377721dc2d51f6ecc55f153a97724d5672e72df807a889b380320a98caf62")
    version("0.5.0", sha256="fc2106f420e7348417249be219f6eb6db2ec8f06969dd63e24b24a2284361e61")
    version("0.4.0", sha256="d354dab59860d8939bbed158ff1adf7a59c41225671e633a51246ab7dbbeeedb")
    version("develop", branch="master")

    depends_on("r@3.6.0:")
    depends_on("r-magrittr")
    depends_on("r-dplyr")
    depends_on("r-ggplot2")
    depends_on("r-tibble")
    depends_on("r-tidyr")
    depends_on("r-patchwork")
    depends_on("r-purrr")
    depends_on("r-readr@1.4.0:")
    depends_on("r-stringr")
    depends_on("r-yaml")
    depends_on("r-lpsolve")
    depends_on("r-gtools")
    depends_on("r-data-tree")
    depends_on("r-zoo")
    depends_on("r-arrow+notcran@3.0.0:")
    depends_on("r-rcpp@1.0.6:")
    depends_on("r-bh")

    patch("patch-Renv.patch", when="@:0.7.1")
