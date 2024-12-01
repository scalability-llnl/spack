# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RA4preproc(RPackage):
    """Automated Affymetrix Array Analysis Preprocessing Package.

    Utility functions to pre-process data for the Automated Affymetrix Array
    Analysis set of packages."""

    bioc = "a4Preproc"

    version("1.48.0", commit="d3bf8b82d7cabd2ef77253bb9a741dcde3ca3a41")
    version("1.46.0", commit="8463958692c73fd655a6dfec39ea99c915513719")
    version("1.44.0", commit="252381265b96b83803a93e0c2014dd6b0574e57f")
    version("1.42.0", commit="773a91e884d2ada16fe9cf57d5ed53c0155e3fa2")
    version("1.38.0", commit="c93c223bd531bff090531a109b51f8dcd710d0cb")
    version("1.32.0", commit="0da742e500892b682feeb39256906282ad20c558")
    version("1.30.0", commit="e6fb9fa2e7c703974e6ca10c0e9681b097b05978")
    version("1.28.0", commit="435d66727f1187020d034a1beaf4cd8bd4f76981")
    version("1.26.0", commit="be7403acc06670c05ead1adaf60533b0fe3a65ea")
    version("1.24.0", commit="651014b8102807aea4f1274e34e083e70b5e7ee7")

    depends_on("r-biocgenerics", type=("build", "run"), when="@1.38.0:")
    depends_on("r-biobase", type=("build", "run"), when="@1.38.0:")

    depends_on("r-annotationdbi", type=("build", "run"), when="@:1.32.0")
