# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQuantro(RPackage):
    """A test for when to use quantile normalization.

    A data-driven test for the assumptions of quantile normalization using
    raw data such as objects that inherit eSets (e.g. ExpressionSet,
    MethylSet). Group level information about each sample (such as Tumor /
    Normal status) must also be provided because the test assesses if there
    are global differences in the distributions between the user-defined
    groups."""

    bioc = "quantro"

    version("1.34.0", commit="c769d21ce5ccb6f33c35e6e1dbb901ea8afad4b1")
    version("1.32.0", commit="0c70b787866d915abb720f2ab326a83eb1e775b7")
    version("1.30.0", commit="e756c439cdc5a6fb4d7879aff56a8368475513b5")
    version("1.28.0", commit="109e7452a349f273e10d2ffb79d5624260b67dd5")
    version("1.24.0", commit="c7c0180292156a01722d91b353da44324e72d68f")
    version("1.18.0", commit="f6553c2296289eed31e4b2f32a082e990bdb8359")
    version("1.16.0", commit="cfc2e853bdc3cc90fd35e153fe243892d50d61c6")
    version("1.14.0", commit="2d43264b2a95ae8ca51a69d7768fe43b9f1b77bb")
    version("1.12.0", commit="1cfcc73875cf4ecc2618e5e45fda89bd075a5d12")
    version("1.10.0", commit="111337c0aba052aa49c3d2e2d3042794b28858c9")

    depends_on("r@3.1.3:", type=("build", "run"))
    depends_on("r@4.0:", type=("build", "run"), when="@1.24.0:")
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-minfi", type=("build", "run"))
    depends_on("r-doparallel", type=("build", "run"))
    depends_on("r-foreach", type=("build", "run"))
    depends_on("r-iterators", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
