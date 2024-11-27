# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffypdnn(RPackage):
    """Probe Dependent Nearest Neighbours (PDNN) for the affy package.

    The package contains functions to perform the PDNN method described by
    Li Zhang et al."""

    bioc = "affypdnn"

    version("1.58.0", commit="83d8b6b0d9606845bd77dbf7164dd5b160f32ccf")
    version("1.56.0", commit="5fd9c5265fb895a1f646cf72e8d5169669d979f2")
    version("1.54.0", commit="ea971b1b9cc443695a6614bef92e8e116ee87d55")
    version("1.52.0", commit="17d74c593ce4f0dfd43f13a5016e482c1399d21e")
    version("1.50.0", commit="97ff68e9f51f31333c0330435ea23b212b3ed18a")

    depends_on("r@2.13.0:", type=("build", "run"))
    depends_on("r-affy@1.5:", type=("build", "run"))
