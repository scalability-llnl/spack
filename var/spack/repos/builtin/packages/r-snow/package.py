# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSnow(RPackage):
    """Simple Network of Workstations.

    Support for simple parallel computing in R."""

    cran = "snow"

    license("GPL-2.0-or-later")

    version("0.4-4", sha256="84587f46f222a96f3e2fde10ad6ec6ddbd878f4e917cd926d632f61a87db13c9")
    version("0.4-3", sha256="8512537daf334ea2b8074dbb80cf5e959a403a78d68bc1e97664e8a4f64576d8")
    version("0.4-2", sha256="ee070187aea3607c9ca6235399b3db3e181348692405d038e962e06aefccabd7")

    depends_on("r@2.13.1:", type=("build", "run"))

    @run_after("install")
    def install_wrapper(self):
        mkdir(self.prefix.bin)
        install("inst/RMPISNOW", self.prefix.bin)
