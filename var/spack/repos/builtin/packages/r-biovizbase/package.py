# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiovizbase(RPackage):
    """Basic graphic utilities for visualization of genomic data.

    The biovizBase package is designed to provide a set of utilities, color
    schemes and conventions for genomic data. It serves as the base for
    various high-level packages for biological data visualization. This
    saves development effort and encourages consistency."""

    bioc = "biovizBase"

    version("1.48.0", commit="534db77074710dae57ade81844c769fd35a2fa9c")
    version("1.46.0", commit="a47060cfb68e3f3b4876114af932823aed5d2d57")
    version("1.44.0", commit="a8f05c56c27b278524033cb896a6c97f3ee0081c")
    version("1.42.0", commit="f1627b2b567471837daca6e763acfc3e13937461")
    version("1.38.0", commit="d0f3362e0ad0e90b4b1d3e47b13ed57907d03403")
    version("1.32.0", commit="de044bf236cdcd71214ae7b77689a8f0ab4f5cc8")
    version("1.30.1", commit="b6776d0470e2920f71127652f185f68ca1fd2c82")
    version("1.28.2", commit="43d09060028665a237b04bfeb9e2575782b08063")
    version("1.26.0", commit="640742f48384f01d117b70dc5c64737e97ae9b4b")
    version("1.24.0", commit="ae9cd2ff665b74a8f45ed9c1d17fc0a778b4af6c")

    depends_on("c", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.38.0:")
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-hmisc", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-dichromat", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-s4vectors@0.9.25:", type=("build", "run"))
    depends_on("r-s4vectors@0.23.19:", type=("build", "run"), when="@1.38.0:")
    depends_on("r-iranges@1.99.28:", type=("build", "run"))
    depends_on("r-genomeinfodb@1.5.14:", type=("build", "run"))
    depends_on("r-genomicranges@1.23.21:", type=("build", "run"))
    depends_on("r-summarizedexperiment", type=("build", "run"))
    depends_on("r-biostrings@2.33.11:", type=("build", "run"))
    depends_on("r-rsamtools@1.17.28:", type=("build", "run"))
    depends_on("r-genomicalignments@1.1.16:", type=("build", "run"))
    depends_on("r-genomicfeatures@1.21.19:", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-variantannotation@1.11.4:", type=("build", "run"))
    depends_on("r-ensembldb@1.99.13:", type=("build", "run"))
    depends_on("r-annotationfilter@0.99.8:", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@1.28.2:")
