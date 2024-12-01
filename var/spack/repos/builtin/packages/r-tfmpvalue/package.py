# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTfmpvalue(RPackage):
    """Efficient and Accurate P-Value Computation for Position Weight Matrices.

    In putative Transcription Factor Binding Sites (TFBSs) identification from
    sequence/alignments, we are interested in the significance of certain match
    score. TFMPvalue provides the accurate calculation of P-value with score
    threshold for Position Weight Matrices, or the score with given P-value.
    This package is an interface to code originally made available by Helene
    Touzet and Jean-Stephane Varre, 2007, Algorithms Mol Biol:2, 15."""

    cran = "TFMPvalue"

    version("0.0.9", sha256="b9db56e75e2cee840d8b7861686dec07ee2c40cbc7d55361e5d04f1bf0c65de7")
    version("0.0.8", sha256="6d052529f7b59d0384edc097f724f70468013777b6adf4c63e61a359029d3841")
    version("0.0.6", sha256="cee3aa2d4e22856865d820f695e29a5f23486e5e08cd42cb95a0728f5f9522a1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@3.0.1:", type=("build", "run"))
    depends_on("r-rcpp@0.11.1:", type=("build", "run"))
