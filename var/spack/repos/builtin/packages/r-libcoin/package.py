# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLibcoin(RPackage):
    """Linear Test Statistics for Permutation Inference.

    Basic infrastructure for linear test statistics and permutation inference
    in the framework of Strasser and Weber (1999) <https://epub.wu.ac.at/102/>.
    This package must not be used by end-users.  CRAN package 'coin' implements
    all user interfaces and is ready to be used by anyone."""

    cran = "libcoin"

    license("GPL-2.0-only")

    version("1.0-10", sha256="3023e0495d0789765bdf04c0ef0990a57b48fefa322c55f20e250d2d70d67eaf")
    version("1.0-9", sha256="2d7dd0b7c6dfc20472430570419ea36a714da7bbafd336da1fb53c5c6463d9eb")
    version("1.0-6", sha256="48afc1415fc89b29e4f2c8b6f6db3cffef1531580e5c806ad7cacf4afe6a4e5a")
    version("1.0-4", sha256="91dcbaa0ab8c2109aa54c3eda29ad0acd67c870efcda208e27acce9d641c09c5")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r-mvtnorm", type=("build", "run"))
