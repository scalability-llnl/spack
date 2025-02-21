# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RErgm(RPackage):
    """Fit, Simulate and Diagnose Exponential-Family Models for Networks.

    An integrated set of tools to analyze and simulate networks based on
    exponential-family random graph models (ERGMs). 'ergm' is a part of the
    Statnet suite of packages for network analysis. See Hunter, Handcock,
    Butts, Goodreau, and Morris (2008) <doi:10.18637/jss.v024.i03> and
    Krivitsky, Hunter, Morris, and Klumb (2021) <arXiv:2106.04997>."""

    cran = "ergm"

    license("GPL-3.0-only")

    version("4.6.0", sha256="b471a60c39eb5b478e06dd0caf1d085f4b0927f1c260de699f1c8d4fe831a7f7")
    version("4.4.0", sha256="2db152cc7fdd71d6f0065603405f30bf5e206591da39b8f542178ec6d6126173")
    version("4.3.1", sha256="3ff63c81ea4061ac0c79247fcd2e614494624f7f1df57a4634927e7e90800ed3")
    version("4.2.3", sha256="35d15373d4a8445872eb3713c81c6c6ac34b72096e0cdb04292a468e65ae9288")
    version("4.2.2", sha256="ced92b0a32c78c85546d665c32fb3993fe77a3809aa88f43c3eee39e2577f2f0")
    version("4.2.1", sha256="484769eb69d127a9e9adf5c1c8c88106d5fbaf4aaf2f915621d7f043c7cab0f5")
    version("4.1.2", sha256="1abc6ef53376a4132530c376ce477ae7a2590e95fe8feb011c0da9cfb4d49ba0")
    version("3.11.0", sha256="4e5506b44badc2343be3657acbf2bca51b47d7c187ff499d5a5e70a9811fe9f2")
    version("3.10.4", sha256="885f0b1a23c5a2c1947962350cfab66683dfdfd1db173c115e90396d00831f22")
    version("3.10.1", sha256="a2ac249ff07ba55b3359242f20389a892543b4fff5956d74143d2d41fa6d4beb")
    version("3.7.1", sha256="91dd011953b93ecb2b84bb3ababe7bddae25d9d86e69337156effd1da84b54c3")

    depends_on("r@3.5:", type=("build", "run"), when="@4.1.2:")
    depends_on("r@4.0:", type=("build", "run"), when="@4.2.1:")
    depends_on("r@4.1:", type=("build", "run"), when="@4.4.0:")
    depends_on("r-network@1.15:", type=("build", "run"))
    depends_on("r-network@1.17:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-network@1.17.0:", type=("build", "run"), when="@4.2.3:")
    depends_on("r-network@1.18.0:", type=("build", "run"), when="@4.4.0:")
    depends_on("r-robustbase@0.93-5:", type=("build", "run"))
    depends_on("r-robustbase@0.93-7:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-coda@0.19-2:", type=("build", "run"))
    depends_on("r-coda@0.19-4:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-trust@0.1.7:", type=("build", "run"))
    depends_on("r-trust@0.1.8:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-matrix@1.2-17:", type=("build", "run"))
    depends_on("r-matrix@1.3-2:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-lpsolveapi@5.5.2.0.17.7:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-mass@7.3-51.4:", type=("build", "run"))
    depends_on("r-mass@7.3.53.1:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-statnet-common@4.3.0:", type=("build", "run"))
    depends_on("r-statnet-common@4.4.0:", type=("build", "run"), when="@3.11.0:")
    depends_on("r-statnet-common@4.5.0:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-statnet-common@4.6.0:", type=("build", "run"), when="@4.2.1:")
    depends_on("r-statnet-common@4.7.0:", type=("build", "run"), when="@4.3.1:")
    depends_on("r-statnet-common@4.8.0:", type=("build", "run"), when="@4.4.0:")
    depends_on("r-statnet-common@4.9.0:", type=("build", "run"), when="@4.5.0:")
    depends_on("r-rle", type=("build", "run"), when="@3.11.0:")
    depends_on("r-rle@0.9.2:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-purrr@0.3.2:", type=("build", "run"), when="@3.10.0:")
    depends_on("r-purrr@0.3.4:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-rlang@0.3.4:", type=("build", "run"), when="@3.10.0:")
    depends_on("r-rlang@0.4.10:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-memoise@2.0.0:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-tibble@2.1.1:", type=("build", "run"), when="@3.10.0:")
    depends_on("r-tibble@3.1.0:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-magrittr@2.0.1:", type=("build", "run"), when="@4.2.1:")
    depends_on("r-rdpack@2.4:", type=("build", "run"), when="@4.4.0:")
    depends_on("r-knitr", type=("build", "run"), when="@4.2.1:")
    depends_on("r-stringr", type=("build", "run"), when="@4.2.1:")

    depends_on("r-dplyr@0.8.0.1:", type=("build", "run"), when="@3.10.0:3.10.4")
    depends_on("r-lpsolve@5.6.13:", type=("build", "run"), when="@:3.11.0")
    depends_on("r-digest", type=("build", "run"), when="@4.2.1:4.2.2")

    # The CRAN page list OpenMPI as a dependency but this is not a dependency
    # for using the package. If one wishes to use MPI, simply load an MPI
    # package, along with r-dosnow and r-rmpi when using r-ergm, and set the
    # appropriate options in the R script.
