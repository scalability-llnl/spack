# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNmof(RPackage):
    """Numerical Methods and Optimization in Finance.

    Functions, examples and data from the book "Numerical Methods and
    Optimization in Finance" by M. Gilli, D. Maringer and E. Schumann (2011),
    ISBN 978-0123756626. The package provides implementations of several
    optimisation heuristics, such as Differential Evolution, Genetic Algorithms
    and Threshold Accepting. There are also functions for the valuation of
    financial instruments, such as bonds and options, and functions that help
    with stochastic simulations."""

    cran = "NMOF"

    version("2.8-0", sha256="6dc53a9be41e673e9b2fcb2783aa82090db5455f079b8aac4c388d679f6ec28a")
    version("2.7-1", sha256="b03e309df35b3fb0980c8a171e1cd1c69739fa6ab7a8992c043166fae4644e23")
    version("2.7-0", sha256="11eeda730262418f22d24d8f72d363a05ac4c3c1130b88f4eafb1b8d81c83160")
    version("2.5-1", sha256="0468ba72364cbdf90781824dfb1a60324203e2248d93cb6f1ffd6eb0d271f390")
    version("2.5-0", sha256="f44914c86d86c62f74cbc026179a694f0b3c2e3341b076acaf5de01de194a3c7")
    version("2.2-2", sha256="e64472f89023f0d779a35df753747d750174ce89644a9142312a1d2dc6f24642")
    version("1.6-0", sha256="5484cd43c28aaf23d560c2dde8bcd8dd440a205d2214eb50e02fe0bb42ec2755")

    depends_on("r@2.14:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@2.8-0:")
