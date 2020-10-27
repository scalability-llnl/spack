# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tealdeer(CargoPackage):
    """Fetch and show tldr help pages for many CLI commands. Full featured
    offline client with caching support."""

    homepage  = "https://github.com/dbrgn/tealdeer/"
    crates_io = "tealdeer"
    git       = "https://github.com/dbrgn/tealdeer.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('1.4.1', sha256='07b2cea274043201ba04aa4a7d741df93db81ba9562a9c9bbfeceb2ca6218e33')
