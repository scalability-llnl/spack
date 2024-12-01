# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RA4classif(RPackage):
    """Automated Affymetrix Array Analysis Classification Package.

    Functionalities for classification of Affymetrix microarray data,
    integrating within the Automated Affymetrix Array Analysis set of
    packages."""

    bioc = "a4Classif"

    version("1.48.0", commit="1e2ff90d5af6332beac630395a7494c8fd30aff4")
    version("1.46.0", commit="96794183a76ab7da7a1863ccd421640254447af5")
    version("1.44.0", commit="df0fce781f9bc480a1159d958c9a63c314a9ed01")
    version("1.42.0", commit="820854a7ca9ed0c295479a25b7e3375c6d01d0b5")
    version("1.38.0", commit="c4d058813efb835774813b2d69c52912162f8e75")
    version("1.32.0", commit="aa4f22df2da54b71e1a238d2b9cbcb3afa6f7f88")
    version("1.30.0", commit="b62841bff2f8894a3011a4e74afc37076d1322a3")
    version("1.28.0", commit="3464011f6c3ddb41b78acc47e775539034287be7")
    version("1.26.0", commit="bc4018c3c441e1840bb3e2959c07611489439a50")
    version("1.24.0", commit="ca06bf274c87a73fc12c29a6eea4b90289fe30b1")

    depends_on("r-a4core", type=("build", "run"))
    depends_on("r-a4preproc", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"), when="@1.38.0:")
    depends_on("r-rocr", type=("build", "run"))
    depends_on("r-pamr", type=("build", "run"))
    depends_on("r-glmnet", type=("build", "run"))
    depends_on("r-varselrf", type=("build", "run"))

    depends_on("r-mlinterfaces", type=("build", "run"), when="@:1.32.0")
