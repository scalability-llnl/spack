# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMrinstruments(RPackage):
    """Data sources for genetic instruments to be used in MR.

    Datasets of eQTLs, GWAS catalogs, etc."""

    homepage = "https://github.com/MRCIEU/MRInstruments"
    url = "https://github.com/MRCIEU/MRInstruments/archive/refs/tags/0.3.3.tar.gz"

    version("0.3.3", sha256="4ddbaf6335133e8f7baef469d6bc1f89212462b9f4062c9e4ddda37b12eb3486")

    depends_on("r@2.10:", type=("build", "run"))
