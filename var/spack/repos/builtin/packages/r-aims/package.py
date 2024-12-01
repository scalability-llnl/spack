# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAims(RPackage):
    """Absolute Assignment of Breast Cancer Intrinsic Molecular Subtype.

    This package contains the AIMS implementation. It contains necessary
    functions to assign the five intrinsic molecular subtypes (Luminal A,
    Luminal B, Her2-enriched, Basal-like, Normal-like). Assignments could be
    done on individual samples as well as on dataset of gene expression
    data."""

    bioc = "AIMS"

    version("1.32.0", commit="019415a6362e805465d43c157606e1774aed9e51")
    version("1.30.0", commit="2ab61159c5aa0902cc33fc1502f7853b66912cce")
    version("1.28.0", commit="84608df638b5694c08158ed77ad2c8a64c4e594b")
    version("1.26.0", commit="5dcf60eb4cdcf563ea848482c9c488f465c27bbd")
    version("1.22.0", commit="34a38978b24377abb864eff7683bb36344ff171d")
    version("1.16.0", commit="86cb8c998ade3003cd34a5405b218ae07d97bf84")
    version("1.14.1", commit="4125c4217a7e4f00169b5ba65dcc3778fdd33c6f")
    version("1.12.0", commit="d7eaa723d19a6aca37df244fd0b3d5426ed0a626")
    version("1.10.0", commit="972945980b39168502a02ac3aa396f9b99fb3d71")
    version("1.8.0", commit="86b866c20e191047492c51b43e3f73082c3f8357")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-e1071", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
