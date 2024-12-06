# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REmmli(RPackage):
    """A Maximum Likelihood Approach to the Analysis of Modularity.

    Fit models of modularity to morphological landmarks. Perform model
    selection on results. Fit models with a single within-module correlation or
    with separate within-module correlations fitted to each module."""

    cran = "EMMLi"

    version("0.0.3", sha256="57c04953200d2253bc90b0035dc590179d1b959768bfa7fdac92b6bcbf9f66ac")
