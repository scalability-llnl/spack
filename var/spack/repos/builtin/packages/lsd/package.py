# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lsd(CargoPackage):
    """
    LSD (LSDeluxe)

    The next gen ls command
    """

    homepage = "https://github.com/peltoche/lsd"
    crates_io = "lsd"
    git = "https://github.com/peltoche/lsd.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.18.0', sha256='6f3536fe6731d70f967286669c5d1acb13f2d95cf481bee1064e2a81a50b774d')
