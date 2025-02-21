# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RWgcna(RPackage):
    """Weighted Correlation Network Analysis.

    Functions necessary to perform Weighted Correlation Network Analysis on
    high-dimensional data as originally described in Horvath and Zhang (2005)
    <doi:10.2202/1544-6115.1128> and Langfelder and Horvath (2008)
    <doi:10.1186/1471-2105-9-559>. Includes functions for rudimentary data
    cleaning, construction of correlation networks, module identification,
    summarization, and relating of variables and modules to sample traits. Also
    includes a number of utility functions for data manipulation and
    visualization."""

    cran = "WGCNA"

    version("1.72-5", sha256="03439143ff235c17f0dbca7dd6362afa8ddb5a72594f5c2df1c6df1caca2e79d")
    version("1.72-1", sha256="1dbf82761ef3e76464b18fc9f698ad0f971aafecabf66ca937b950930bd57fdc")
    version("1.71", sha256="21f5349e888ea76241912600ee5c35a0d2fd50180568b9b08b2b597f099bf708")
    version("1.70-3", sha256="b9843b839728183af6b746f239e9519d438b294613362b556002acdb8522cbd4")
    version("1.69", sha256="2ea152d45b2d4f0e40b4b9f7b5ea8a96e230f7744ece8be27bdba96cf39d5008")
    version("1.68", sha256="0a04f15a20817f9260ae1896eda3be83a7f4855a27a348df85c7f4d376f1efe8")
    version("1.67", sha256="c9cc9989763b2c80835489eabd38d9ee35b204305044d115ca7c775a103f6824")
    version("1.64-1", sha256="961a890cda40676ba533cd6de2b1d4f692addd16363f874c82ba8b65dd2d0db6")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r-dynamictreecut@1.62:", type=("build", "run"))
    depends_on("r-fastcluster", type=("build", "run"))
    depends_on("r-matrixstats@0.8.1:", type=("build", "run"))
    depends_on("r-hmisc", type=("build", "run"))
    depends_on("r-impute", type=("build", "run"))
    depends_on("r-foreach", type=("build", "run"))
    depends_on("r-doparallel", type=("build", "run"))
    depends_on("r-preprocesscore", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"))
    depends_on("r-go-db", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-rcpp@0.11.0:", type=("build", "run"))

    depends_on("r-robust", type=("build", "run"), when="@:1.68")
