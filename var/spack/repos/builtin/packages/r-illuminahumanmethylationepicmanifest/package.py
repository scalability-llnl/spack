# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIlluminahumanmethylationepicmanifest(RPackage):
    """Manifest for Illumina's EPIC methylation arrays."""

    bioc = "IlluminaHumanMethylationEPICmanifest"
    url = "https://bioconductor.org/packages/release/data/annotation/src/contrib/IlluminaHumanMethylationEPICmanifest_0.3.0.tar.gz"

    version("0.3.0", sha256="e39a69d98486cec981e97c56f45bbe47d2ccb5bbb66a1b16fa0685575493902a")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-minfi", type=("build", "run"))
