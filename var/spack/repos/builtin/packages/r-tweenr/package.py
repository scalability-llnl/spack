# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTweenr(RPackage):
    """Interpolate Data for Smooth Animations.

    In order to create smooth animation between states of data, tweening is
    necessary. This package provides a range of functions for creating tweened
    data that can be used as basis for animation. Furthermore it adds a number
    of vectorized interpolaters for common R data types such as numeric, date
    and colour."""

    cran = "tweenr"

    license("MIT")

    version("2.0.3", sha256="efabe512a45d653787ba40f87f3e23add4037f88573a102fa9ac7a5ff43c8cbe")
    version("2.0.2", sha256="64bbfded418d4880e3636f434571c20303d2f66be6950d64583a864fbb661ff3")
    version("1.0.2", sha256="1805f575da6705ca4e5ec1c4605222fc826ba806d9ff9af41770294fe08ff69f")
    version("1.0.1", sha256="efd68162cd6d5a4f6d833dbf785a2bbce1cb7b9f90ba3fb060931a4bd705096b")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-farver", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-cpp11@0.4.2:", type=("build", "run"), when="@2.0.2:")
    depends_on("r-vctrs", type=("build", "run"), when="@2.0.2:")
    depends_on("r-rcpp@0.12.3:", type=("build", "run"), when="@:1.0.2")
