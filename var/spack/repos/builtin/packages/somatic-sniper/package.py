# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SomaticSniper(CMakePackage):
    """A tool to call somatic single nucleotide variants."""

    homepage = "https://gmt.genome.wustl.edu/packages/somatic-sniper"
    url = "https://github.com/genome/somatic-sniper/archive/v1.0.5.0.tar.gz"

    license("MIT")

    version("1.0.5.0", sha256="fc41e90237b059fcc591e404830c4b1be678642dd5afd76ce545b97b4b7b3de1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("ncurses")

    parallel = False
