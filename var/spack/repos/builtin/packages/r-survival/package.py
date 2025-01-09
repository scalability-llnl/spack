# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSurvival(RPackage):
    """Survival Analysis.

    Contains the core survival analysis routines, including definition of Surv
    objects, Kaplan-Meier and Aalen-Johansen (multi-state) curves, Cox models,
    and parametric accelerated failure time models."""

    cran = "survival"

    license("LGPL-2.0-or-later")

    version("3.7-0", sha256="cd96b08ec928b0028f69c942cc788e190b4543c8518d71deb6d8a712de44feef")
    version("3.5-5", sha256="1375a509554b0258e04e27baca2e073e179406e2a9a71e6d3e0c777072568476")
    version("3.4-0", sha256="a48e23d47265fe4d90fb5f0f9fc388906014f8063211980856985db9e89cf812")
    version("3.3-1", sha256="14878705cd0c7edcfead79011444aa84f680759293bde8634721c49f37cb4dc7")
    version("3.2-13", sha256="3fab9c0ba2c4e2b6a475207e2629a7f06a104c70093dfb768f50a7caac9a317f")
    version("3.2-7", sha256="5356cd73da7ecfda4042e8a8ae00d3531b106f7b39ca31a1843eadf288418a46")
    version("3.1-12", sha256="b62ed66eb646f3df13f7e9bf6571e3bfecae128c66491e174c8833cbef1bf21f")
    version("2.44-1.1", sha256="55b151e15fcd24ccb3acf60331c9a7ad82bc10f3841ab3be9bc2a37e9ee751b9")
    version("2.44-1", sha256="82c44afa41fe4504295855f1da4a5940c3289dfd61bc664bf211bb67c051a909")
    version("2.41-3", sha256="f3797c344de93abd2ba8c89568770a13524a8b2694144ae55adec46921c8961d")
    version("2.40-1", sha256="91d5217847e39bebcbce4f0a2e295304e5816b1270e71f5f2ed39807f004ee82")
    version("2.39-5", sha256="607170ebe36080d102e884cf13c3b29df01d6bb3b593258afffa67fee2a0ada7")

    depends_on("r@2.13.0:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@3.1-12:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@3.2-13:")
    depends_on("r-matrix", type=("build", "run"))
