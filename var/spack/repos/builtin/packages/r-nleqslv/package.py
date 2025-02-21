# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNleqslv(RPackage):
    """Solve Systems of Nonlinear Equations.

    Solve a system of nonlinear equations using a Broyden or a Newton method
    with a choice of global strategies such as line search and trust region.
    There are options for using a numerical or user supplied Jacobian, for
    specifying a banded numerical Jacobian and for allowing a singular or
    ill-conditioned Jacobian."""

    cran = "nleqslv"

    license("GPL-2.0-or-later")

    version("3.3.5", sha256="1298172d2fe67d8d6b742ce7e792f6b897f081da5c94d34f14970ab531f04b3a")
    version("3.3.4", sha256="2783e7525bcd155dd8cedf5a41b7db65cd1fa0e095cd937371448316f3930fcf")
    version("3.3.3", sha256="2e46dfce95ddfd7ed5208413ee41f6bdf1ae18414fb1d0c146d9da3af12ac633")
    version("3.3.2", sha256="f54956cf67f9970bb3c6803684c84a27ac78165055745e444efc45cfecb63fed")
