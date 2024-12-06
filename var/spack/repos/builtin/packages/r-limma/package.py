# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLimma(RPackage):
    """Linear Models for Microarray Data.

    Data analysis, linear models and differential expression for microarray
    data."""

    bioc = "limma"

    version("3.56.0", commit="efe857829233edb11ae317ce5d1ad4ea3073cf7f")
    version("3.54.0", commit="1d1fa843d4fe2f8c94fd843bb1e80b8384d8306e")
    version("3.52.4", commit="3226c29ad8c18aa7e6722f4a2c95ff8ac900437e")
    version("3.52.1", commit="c81c539a217ac1cf46e850f8a20266cecfafed50")
    version("3.50.0", commit="657b19bbc33c5c941af79aeb68967bf42ea40e23")
    version("3.46.0", commit="ff03542231827f39ebde6464cdbba0110e24364e")
    version("3.40.6", commit="3ae0767ecf7a764030e7b7d0b1d0f292c0b24055")
    version("3.38.3", commit="77b292eb150cdedaa1db704bcfb01f0bb29e9849")
    version("3.36.5", commit="3148d1cb7eea9c6bdd60351d51abcfd665332d44")
    version("3.34.9", commit="6755278a929f942a49e2441fb002a3ed393e1139")
    version("3.32.10", commit="593edf28e21fe054d64137ae271b8a52ab05bc60")

    depends_on("c", type="build")  # generated

    depends_on("r@2.3.0:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@3.40.6:")
