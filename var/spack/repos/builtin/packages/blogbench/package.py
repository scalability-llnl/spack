# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Blogbench(AutotoolsPackage):
    """A filesystem benchmark tool that simulates a realistic load."""

    homepage = "https://openbenchmarking.org/test/pts/blogbench"
    url      = "http://download.pureftpd.org/pub/blogbench/blogbench-1.1.tar.gz"

    version('1.1', sha256='8cded059bfdbccb7be35bb6a2272ecfdbe3fbea43d53c92ba5572ac24f26c4df')
    version('1.0', sha256='dc29261a19064a8fb64d39b27607f19d3b33ce3795908e717404167687ef33be')
