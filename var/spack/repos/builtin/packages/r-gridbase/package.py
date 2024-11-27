# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGridbase(RPackage):
    """Integration of base and grid graphics."""

    cran = "gridBase"

    version("0.4-7", sha256="be8718d24cd10f6e323dce91b15fc40ed88bccaa26acf3192d5e38fe33e15f26")

    depends_on("r@2.3.0:", type=("build", "run"))
