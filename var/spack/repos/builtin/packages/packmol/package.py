# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Packmol(CMakePackage):
    """Packmol creates an initial point for molecular dynamics simulations
    by packing molecules in defined regions of space."""

    homepage = "https://m3g.iqm.unicamp.br/packmol/home.shtml"
    url = "https://github.com/mcubeg/packmol/archive/18.169.tar.gz"

    license("MIT")

    version("20.0.0", sha256="4faa1c8d5e5db2e935fbc23e7167df7e0b85aa0993c57b74cb897d13e5cf2202")
    version("18.169", sha256="8acf2cbc742a609e763eb00cae55aecd09af2edb4cc4e931706e2f06ac380de9")

    depends_on("fortran", type="build")  # generated
