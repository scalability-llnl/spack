# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLumi(RPackage):
    """BeadArray Specific Methods for Illumina Methylation and Expression
    Microarrays.

    The lumi package provides an integrated solution for the Illumina
    microarray data analysis. It includes functions of Illumina BeadStudio
    (GenomeStudio) data input, quality control, BeadArray-specific variance
    stabilization, normalization and gene annotation at the probe level. It
    also includes the functions of processing Illumina methylation microarrays,
    especially Illumina Infinium methylation microarrays."""

    bioc = "lumi"

    version("2.52.0", commit="c6aa992a622dbaba4dae1b54c61835a37cce8e95")
    version("2.50.0", commit="8711b77a1b5b0a58770d25d3d079ad02208704f5")
    version("2.48.0", commit="1f988ffe04d2c0707b2202d2074d02b679a3204b")
    version("2.46.0", commit="a68932c17a61c99e58ebbd8008d078bec6adb4e7")
    version("2.42.0", commit="a643b3ba46fee951b8566ddd8216af7e6c92f6f6")
    version("2.38.0", commit="321d480d44ce9a0c02ce5af1bddc1f549abdea59")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-biobase@2.5.5:", type=("build", "run"))
    depends_on("r-affy@1.23.4:", type=("build", "run"))
    depends_on("r-methylumi@2.3.2:", type=("build", "run"))
    depends_on("r-genomicfeatures", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-annotate", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-mgcv@1.4-0:", type=("build", "run"))
    depends_on("r-nleqslv", type=("build", "run"))
    depends_on("r-kernsmooth", type=("build", "run"))
    depends_on("r-preprocesscore", type=("build", "run"))
    depends_on("r-rsqlite", type=("build", "run"))
    depends_on("r-dbi", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
