# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Blogbench(AutotoolsPackage):
    """A filesystem benchmark tool that simulates a realistic load."""

    homepage = "https://openbenchmarking.org/test/pts/blogbench"
    url = "https://download.pureftpd.org/pub/blogbench/blogbench-1.1.tar.gz"

    version("1.2", sha256="1eabdb1ac0ad8ff6f5b9de36b2ef9b684a35b6e40aea0424e3dd4d6cd923c1af")
    version("1.1", sha256="8cded059bfdbccb7be35bb6a2272ecfdbe3fbea43d53c92ba5572ac24f26c4df")
    version("1.0", sha256="dc29261a19064a8fb64d39b27607f19d3b33ce3795908e717404167687ef33be")

    depends_on("c", type="build")  # generated
