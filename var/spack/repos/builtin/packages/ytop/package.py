# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ytop(CargoPackage):
    """Another TUI based system monitor, this time in Rust!"""

    homepage  = "https://github.com/cjbassi/ytop"
    crates_io = "ytop"
    git       = "https://github.com/cjbassi/ytop"

    maintainers = ["AndrewGaspar"]

    version('master', branch='master')
    version('0.6.2', sha256='16473b92b115c01faf8dd0b89fd12967684d3a88a5c6047d2f76b2dcfbcb0ed2')
