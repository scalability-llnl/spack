# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FdFind(CargoPackage):
    """A simple, fast and user-friendly alternative to 'find'."""

    homepage = "https://github.com/sharkdp/fd"
    crates_io = "fd-find"
    git = "https://github.com/sharkdp/fd.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('8.1.1', sha256='5549a19f384243f65ed9ef644e88ef1e9146065c5e2224828657cc0b512e8a88')
