# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScaledmatrix(RPackage):
    """Creating a DelayedMatrix of Scaled and Centered Values.

    Provides delayed computation of a matrix of scaled and centered values.
    The result is equivalent to using the scale() function but avoids explicit
    realization of a dense matrix during block processing. This permits greater
    efficiency in common operations, most notably matrix multiplication."""

    bioc = "ScaledMatrix"

    version("1.8.0", commit="122f2c43d496bd420f0aff7cd96728a11bd7fa07")
    version("1.6.0", commit="45a29d3662e2766f973b281ed86ce2654be84b70")
    version("1.4.1", commit="15e2efcb6b11e26c31ef2d44968355f71cc1f4fc")
    version("1.4.0", commit="32e6e918bc7bb64bbf75613d353ca268c7d04292")
    version("1.2.0", commit="d0573e14ca537b40ade7dd1c9cf0cadae60d4349")

    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-delayedarray", type=("build", "run"))
