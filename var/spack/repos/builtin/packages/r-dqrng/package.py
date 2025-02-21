# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDqrng(RPackage):
    """Fast Pseudo Random Number Generators.

    Several fast random number generators are provided as C++ header only
    libraries: The PCG family by O'Neill (2014
    <https://www.cs.hmc.edu/tr/hmc-cs-2014-0905.pdf>) as well as Xoroshiro128+
    and Xoshiro256+ by Blackman and Vigna (2018 <arXiv:1805.01407>). In
    addition fast functions for generating random numbers according to a
    uniform, normal and exponential distribution are included. The latter two
    use the Ziggurat algorithm originally proposed by Marsaglia and Tsang
    (2000, <doi:10.18637/jss.v005.i08>). These functions are exported to R and
    as a C++ interface and are enabled for use with the default 64 bit
    generator from the PCG family, Xoroshiro128+ and Xoshiro256+ as well as the
    64 bit version of the 20 rounds Threefry engine (Salmon et al., 2011
    <doi:10.1145/2063384.2063405>) as provided by the package 'sitmo'."""

    cran = "dqrng"

    license("AGPL-3.0-only OR custom")

    version("0.4.1", sha256="3d9df935020c3c2538bc712456079925c4b379d67407c83fbc008340e353288f")
    version("0.3.0", sha256="4beeabfe245ce7196b07369f2a7d277cb08869ad8b45a22c6354c4cc70a39abb")
    version("0.2.1", sha256="e149c105b1db31e7f46b1aebf31d911a109e380923f3696fc56a53197fc1e866")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.3.1:")
    depends_on("r-rcpp@0.12.16:", type=("build", "run"))
    depends_on("r-bh@1.64.0-1:", type=("build", "run"))
    depends_on("r-sitmo@2.0.0:", type=("build", "run"))
