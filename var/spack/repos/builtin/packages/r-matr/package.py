# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMatr(RPackage):
    """Metagenomics Analysis Tools.

    Package matR (Metagenomics Analysis Tools for R) is an analysis client for
    the MG-RAST metagenome annotation engine, part of the US Department of
    Energy (DOE) Systems Biology Knowledge Base (KBase).  Customized analysis
    and visualization tools securely access remote data and metadata within the
    popular open source R language and environment for statistical
    computing."""

    cran = "matR"

    version("0.9.1", sha256="554aeff37b27d0f17ddeb62b2e1004aa1f29190300e4946b1bec1d7c2bde82e3")
    version("0.9", sha256="5750e6a876cf85fe66038292adefbfcb18e2584fa2e841f39dbe67f3c51b3052")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-mgraster", type=("build", "run"))
    depends_on("r-biom-utils", type=("build", "run"))
