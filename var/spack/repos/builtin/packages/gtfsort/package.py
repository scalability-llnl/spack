# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gtfsort(CargoPackage):
    """A chr/pos/feature GTF sorter that uses a lexicographically-based index ordering algorithm"""

    homepage = "https://github.com/alejandrogzi/gtfsort"
    url = "https://github.com/alejandrogzi/gtfsort/archive/refs/tags/v.0.2.2.tar.gz"

    license("MIT", checked_by="A_N_Other")

    version("0.2.2", sha256="d22a8ef32e30111ad2dd08d1da0e0914ac62a728483b8e39a4ef8ea4e6133b4f")
