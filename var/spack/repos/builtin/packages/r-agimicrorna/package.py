# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAgimicrorna(RPackage):
    """Processing and Differential Expression Analysis of Agilent microRNA
       chips.

    Processing and Analysis of Agilent microRNA data."""

    bioc = "AgiMicroRna"

    version("2.50.0", commit="a812b0f4f215b093ca685889b65de60c6701b695")
    version("2.48.0", commit="4c163b1b730150a3a60a3815bd8c08fa04d71fc1")
    version("2.46.0", commit="8c6d73e1c3f1f9cc019bdb219b19e6179bb1efe4")
    version("2.44.0", commit="8b308baa3b1b0afc0855ea263630a288689e3864")
    version("2.40.0", commit="cfa4acb2215da44767ab3a45845bcd587c309e74")
    version("2.34.0", commit="aaa8cdd70ed2696c313f6240ffbfa044f0d97a7a")
    version("2.32.0", commit="681ae17d07e8e533f798a607b761b71a31f407d8")
    version("2.30.0", commit="99b5a8284cfe3e93c3ae85a2436e87101b9599dd")
    version("2.28.0", commit="62c4a12f1168c7aa1ab46d2c97090ef71478328e")
    version("2.26.0", commit="6dd74bae47986f2a23d03e3f1f9f78f701dd8053")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-limma", type=("build", "run"))
    depends_on("r-affy@1.22:", type=("build", "run"))
    depends_on("r-preprocesscore", type=("build", "run"))
    depends_on("r-affycoretools", type=("build", "run"))
