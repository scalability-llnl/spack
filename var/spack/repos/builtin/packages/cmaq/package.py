# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cmaq(Package):
    """Code base for the U.S. EPA's Community Multiscale Air Quality Model
    (CMAQ)."""

    homepage = "https://www.epa.gov/CMAQ"
    url = "https://github.com/USEPA/CMAQ/archive/CMAQv5.3.1_19Dec2019.tar.gz"

    license("CC0-1.0")

    version(
        "5.3.1",
        sha256="659156bba27f33010e0fdc157a8d33f3b5b779b95511e2ade870284b6bcb4bc8",
        url="https://github.com/USEPA/CMAQ/archive/CMAQv5.3.1_19Dec2019.tar.gz",
    )
    version(
        "5.3",
        sha256="e245c291c7e88d481b13f577d1af9aeb5aef4de8c59f7fa06fa41d19bb2ed18c",
        url="https://github.com/USEPA/CMAQ/archive/CMAQv5.3_27Aug2019.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    def install(self, spec, prefix):
        install_tree(".", prefix)
