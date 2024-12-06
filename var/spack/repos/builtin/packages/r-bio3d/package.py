# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBio3d(RPackage):
    """Biological Structure Analysis.

    Utilities to process, organize and explore protein structure, sequence and
    dynamics data. Features include the ability to read and write structure,
    sequence and dynamic trajectory data, perform sequence and structure
    database searches, data summaries, atom selection, alignment,
    superposition, rigid core identification, clustering, torsion analysis,
    distance matrix analysis, structure and sequence conservation analysis,
    normal mode analysis, principal component analysis of heterogeneous
    structure data, and correlation network analysis from normal mode and
    molecular dynamics data. In addition, various utility functions are
    provided to enable the statistical and graphical power of the R environment
    to work with biological sequence and structural data. Please refer to the
    URLs below for more information."""

    cran = "bio3d"

    license("GPL-2.0-or-later")

    version("2.4-4", sha256="5654eac10d33e4235ef89292e3b99006d8812b6bfaaa3d6fb540312160fd9de9")
    version("2.4-3", sha256="c6031f0d9033260a938171d0fa70720962e352935eb7bd2ddb9b92b93abe6a74")
    version("2.4-2", sha256="91415766cda0f96557e6bc568dbce8d44254a9460f2e2d0beed0ce14ffad6ccb")
    version("2.4-1", sha256="679fbd87fe9fb82a65427d281d3b68906509e411270cd87d2deb95d404333c1f")
    version("2.3-4", sha256="f9b39ab242cbedafcd98c1732cb1f5c0dd9ef66e28be39695e3420dd93e2bafe")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("zlib-api")
