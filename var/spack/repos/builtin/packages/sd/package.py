# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sd(CargoPackage):
    """An intuitive find & replace CLI"""

    homepage  = "https://github.com/chmln/sd"
    crates_io = "sd"
    git       = "https://github.com/chmln/sd.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.7.6', sha256='2bd6da77acacf3aa4cf862c7c19af5985313d8878b1d08f5ac3beead32907bf4')
