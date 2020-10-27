# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hyperfine(CargoPackage):
    """A command-line benchmarking tool"""

    homepage  = "https://github.com/sharkdp/hyperfine"
    crates_io = "hyperfine"
    git       = "https://github.com/sharkdp/hyperfine.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('1.10.0', sha256='d3a10992f4fd470843f823e1e4784f1cd0237708e5158f54d011dac088e9d231')
