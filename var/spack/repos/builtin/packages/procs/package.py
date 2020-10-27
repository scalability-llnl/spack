# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Procs(CargoPackage):
    """A modern replacement for ps"""

    homepage  = "https://crates.io/crates/procs"
    crates_io = "procs"
    git       = "https://github.com/dalance/procs.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.10.4', sha256='e845f509a43c5ce32dc4c3601a6340acd03583e083be2d8f059718e701aaa35d')
