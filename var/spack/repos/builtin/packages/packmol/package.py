# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Packmol(CMakePackage):
    """Packmol creates an initial point for molecular dynamics simulations
    by packing molecules in defined regions of space."""

    homepage = "http://m3g.iqm.unicamp.br/packmol/home.shtml"
    url      = "https://github.com/mcubeg/packmol/archive/18.169.tar.gz"

    version('18.169', sha256='8acf2cbc742a609e763eb00cae55aecd09af2edb4cc4e931706e2f06ac380de9')
