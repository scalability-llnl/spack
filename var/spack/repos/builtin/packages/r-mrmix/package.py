# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMrmix(RPackage):
    """Mendelian Randomization Analysis Using Mixture Models (MRMix).

    This package gives robust estimation of causal effects by conducting
    Mendelian randomization analysis using a mixture model approach."""

    homepage = "https://github.com/gqi/MRMix"
    git = "https://github.com/gqi/MRMix"

    version("0.1.0", commit="56afdb2bc96760842405396f5d3f02e60e305039")
