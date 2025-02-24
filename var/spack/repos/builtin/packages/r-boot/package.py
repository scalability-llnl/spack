# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBoot(RPackage):
    """Bootstrap Functions (Originally by Angelo Canty for S).

    Functions and datasets for bootstrapping from the book "Bootstrap Methods
    and Their Application" by A. C. Davison and D. V. Hinkley (1997, CUP),
    originally written by Angelo Canty for S."""

    cran = "boot"

    license("custom")

    version("1.3-30", sha256="5509d62bd6e6c21b6ef352ab7846d89027bddbfb727fd0cf55da59558bd3fe97")
    version("1.3-28.1", sha256="d4cde76fcc8ccc7ffa329de69147b66a6a93a10188e89342fd18207b1d02ff53")
    version("1.3-28", sha256="9f7158fd2714659f590c3955651893dc24bd8f39196bc5a4cc35b0b031744a32")
    version("1.3-25", sha256="464835fcb453072346ce49e4ae318e04c9dba682349be49db616623b6088fbbe")
    version("1.3-23", sha256="79236a5a770dc8bf5ce25d9aa303c5dc0574d94aa043fd00b8b4c8ccc877357f")
    version("1.3-22", sha256="cf1f0cb1e0a7a36dcb6ae038f5d0211a0e7a009c149bc9d21acb9c58c38b4dfc")
    version("1.3-20", sha256="adcb90b72409705e3f9c69ea6c15673dcb649b464fed06723fe0930beac5212a")
    version("1.3-18", sha256="12fd237f810a69cc8d0a51a67c57eaf9506bf0341c764f8ab7c1feb73722235e")

    depends_on("r@3.0.0:", type=("build", "run"))
