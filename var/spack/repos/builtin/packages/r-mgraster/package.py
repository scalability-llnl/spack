# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMgraster(RPackage):
    """API Client for the MG-RAST Server of the US DOE KBase.

    Convenience Functions for R Language Access to the v.1 API of the MG-RAST
    Metagenome Annotation Server, part of the US Department of Energy (DOE)
    Systems Biology Knowledge Base (KBase)."""

    cran = "MGRASTer"

    version("0.9", sha256="f727b5270ed4bd6dcacaecb49e1ace7eb40827754be9801230db940c4012ae4a")

    depends_on("r@3:", type=("build", "run"))
