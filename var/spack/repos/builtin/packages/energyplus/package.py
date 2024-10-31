# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Energyplus(Package):
    """EnergyPlus is a whole building energy simulation program that engineers,
    architects, and researchers use to model both energy consumption for
    heating, cooling, ventilation, lighting and plug and process loads
    and water use in buildings"""

    homepage = "https://energyplus.net"

    # versions require explicit URLs as they contain hashes
    version(
        "9.3.0",
        sha256="c939dc4f867224e110485a8e0712ce4cfb1e06f8462bc630b54f83a18c93876c",
        url="https://github.com/NREL/EnergyPlus/releases/download/v9.3.0/EnergyPlus-9.3.0-baff08990c-Linux-x86_64.tar.gz",
    )
    version(
        "9.1.0",
        sha256="742b4897781ca8f4b0065c9cd97bf9c5e378968dbb059a21eb91856ba1ec404d",
        url="https://github.com/NREL/EnergyPlus/releases/download/v9.1.0/EnergyPlus-9.1.0-08d2e308bb-Linux-x86_64.tar.gz",
    )
    version(
        "8.9.0",
        sha256="13a5192b25815eb37b3ffd019ce3b99fd9f854935f8cc4362814f41c56e9ca98",
        url="https://github.com/NREL/EnergyPlus/releases/download/v8.9.0-WithIDDFixes/EnergyPlus-8.9.0-eba93e8e1b-Linux-x86_64.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        # binary distribution, we just unpack to lib/energyplus
        # and then symlink the appropriate targets

        # there is only one folder with a semi-predictable name so we glob it
        source_dir = "."

        if spec.satisfies("@:8.9.9"):
            source_dir = glob.glob("EnergyPlus*")[0]

        install_tree(source_dir, prefix.lib.enregyplus)

        mkdirp(prefix.bin)
        for b in ["energyplus", "EPMacro", "ExpandObjects"]:
            os.symlink(join_path(prefix.lib.energyplus, b), join_path(prefix.bin, b))
