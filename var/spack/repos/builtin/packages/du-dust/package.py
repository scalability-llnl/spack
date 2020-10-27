# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DuDust(CargoPackage):
    """A more intuitive version of du"""

    homepage  = "https://github.com/bootandy/dust"
    crates_io = "du-dust"
    git       = "https://github.com/bootandy/dust.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.5.3', sha256='9b05a4cb93aa6d06d473bfd6e5d13392bdb417cd63b5b86608884c4878e09aa6')
