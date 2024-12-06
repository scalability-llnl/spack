# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAnaquin(RPackage):
    """Statistical analysis of sequins.

    The project is intended to support the use of sequins (synthetic
    sequencing spike-in controls) owned and made available by the Garvan
    Institute of Medical Research. The goal is to provide a standard open
    source library for quantitative analysis, modelling and visualization of
    spike-in controls."""

    bioc = "Anaquin"

    version("2.24.0", commit="0eefabdc4036b98505032c460d08375839b1fc3e")
    version("2.22.0", commit="d848a9bd7bf9d1d62202cc477300bf1a65b3e36c")
    version("2.20.0", commit="61598dd3430b09b57f31d7d550ea95126a2d73c8")
    version("2.18.0", commit="c8e3df3e299c32daac0dda23cea59a18673d886b")
    version("2.14.0", commit="d0a34c931a0e72080bff91dacb37dbbe26b45386")
    version("2.8.0", commit="f591d420740b77881ae0a4c16b208c63d460c601")
    version("2.6.1", commit="22b6c71697fe1e2db8f6d18f77728d0fd96fa6d6")
    version("2.4.0", commit="0d6ae80ff622151a782e4774ca274f06024a71d2")
    version("2.2.0", commit="739f4ed2b73c43f934fd65a993ecb48242a5d5da")
    version("1.2.0", commit="584d1970cc9dc1d354f9a6d7c1306bd7e8567119")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r-ggplot2@2.2.0:", type=("build", "run"))
    depends_on("r-rocr", type=("build", "run"))
    depends_on("r-knitr", type=("build", "run"))
    depends_on("r-qvalue", type=("build", "run"))
    depends_on("r-locfit", type=("build", "run"))
    depends_on("r-plyr", type=("build", "run"))
    depends_on("r-deseq2", type=("build", "run"))
